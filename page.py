#!/usr/bin/python
# -*- coding: utf-8 -*-
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import streamlit.components.v1 as components
from configparser import ConfigParser
from pathlib import Path
import streamlit as st
from io import BytesIO
from llms import *
import xlsxwriter
import platform
import base64
import time
import os
import re

# 设置页面配置
st.set_page_config(
    page_title="测试用例生成辅助工具",
    page_icon=":tm:",
    layout="wide"
)

conf = ConfigParser()
pt = platform.system()
main_path = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.ini')


def css_init():
    st.markdown('''<style>
.edw49t12 {
    max-width: 500px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>''', unsafe_allow_html=True)


def session_init():
    if 'run_cases' not in st.session_state:
        st.session_state.run_cases = True


def main():
    if pt in ["Windows", "Darwin"]:  # 添加对macOS(Darwin)的支持
        session_init()  # session缓存初始化
        css_init()  # 前端css样式初始化
        html_init()  # 前端html布局初始化
    else:
        cs_404()
    return None


def cs_404():
    # 背景图片的网址
    img_url = 'https://img.zcool.cn/community/0156cb59439764a8012193a324fdaa.gif'

    # 修改背景样式
    st.markdown('''<span style="color: cyan"> ''' + f"不支持当前系统 {pt} 运行" + '''</span>''', unsafe_allow_html=True)
    st.markdown('''<style>.css-fg4pbf{background-image:url(''' + img_url + ''');
    background-size:100% 100%;background-attachment:fixed;}</style>''', unsafe_allow_html=True)


def img_to_bytes(img_path):
    img_bytes = Path(os.path.join(os.path.split(os.path.realpath(__file__))[0], img_path)).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def read_system_message(filename):
    message_path = os.path.join(main_path, filename)
    with open(message_path, "r", encoding="utf8") as f:  # 打开文件
        data = f.read()  # 读取文件
        return data


# 创建测试用例生成器代理
@st.cache_resource
def get_testcase_writer(llm_config, system_message):
    return AssistantAgent(
        name="testcase_writer",
        llm_config=llm_config,
        system_message=system_message,
    )


# 创建评审用例生成器代理
@st.cache_resource
def get_testcase_reader(llm_config, system_message):
    return AssistantAgent(
        name="critic",
        llm_config=llm_config,
        system_message=system_message,
    )


# 用例格式化
@st.cache_resource
def format_testcases(raw_output):
    cases = re.findall(r'(\|.+\|)', raw_output, re.IGNORECASE)
    new_cases = list(dict.fromkeys(cases))
    return new_cases


def html_init():
    js_code = '''
    $(document).ready(function(){
        $("footer", window.parent.document).remove()
    });
    '''
    # 引用了JQuery v2.2.4
    components.html(f'''<script src="https://cdn.bootcdn.net/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
        <script>{js_code}</script>''', width=0, height=0)
    # sidebar图标
    st.sidebar.markdown(
        '''<a href="#"><img src='data:image/png;base64,{}' class='img-fluid' width=40 height=40 target='_self'></a>'''.format(
            img_to_bytes("img/Jack.png")), unsafe_allow_html=True)

    # sidebar.expander
    with st.sidebar:
        expander1 = st.expander("使用说明", True)
        with expander1:
            st.markdown(
                """
            👉<a href="https://github.com/13429837441/AutoGenTestCase/blob/main/README.md" target='blank'>模型ApiKey申请说明</a>👈
            ### **使用步骤**
            ##### 1、上传文件（.txt）或手动输入需求描述
            ##### 2、设置高级选项设置
            ##### 3、点击"生成测试用例"按钮
            ##### 4、查看生成的测试用例
            ##### 5、下载测试用例文件
            
            ### **高级选项设置**
            ##### **用例分类**：选择用例类型（功能验证用例、边界用例、异常场景用例、性能/兼容性用例、回归测试用例）
            ##### **用例优先级**：设置整体用例的优先级
            """
            , unsafe_allow_html=True)

        expander2 = st.expander("关于", False)
        with expander2:
            st.markdown(
                """
                ###### 本工具使用到的AI工具包括（DeepSeek、通义千问）
                ###### AI工具生成的测试用例可作为参考使用，具体业务还需要人工干预并进行补充
                ###### 本工具是利用deepseek写测试用例，通义千问负责用例评审
                """
            )
    # sidebar标题
    st.sidebar.markdown("---")

    st.sidebar.markdown('''<small style='float: right'>By <a id="reload" href="#公众号：One Little Testing" title="公众号：One Little Testing">@Jack</a></small>''',
                        unsafe_allow_html=True)

    # 读取配置
    conf.read(config_path)
    deep_base_url_list = conf['deepseek']['base_url_list'].split(",")
    qwen_base_url_list = conf['qwen']['base_url_list'].split(",")
    deep_model_list = conf['deepseek']['model_list'].split(",")
    qwen_model_list = conf['qwen']['model_list'].split(",")
    # main主页面
    source_tab1, source_tab2 = st.tabs(["⚙AI模型设置", "🖥 AI交互"])
    # AI模型设置
    with source_tab1:
        st.subheader("DeepSeek模型配置【单角色：编写用例】")
        ai1 = st.checkbox("deepseek", eval(conf['deepseek']['choice']))
        cols1 = st.columns([2, 2, 2])
        if ai1:
            api_key_1 = cols1[0].text_input("deepseek_api_key",
                                            placeholder="sk-xxxxxxxxxxxxx",
                                            value=conf['deepseek']['api_key'])
            base_url_1 = cols1[1].selectbox("base_url", deep_base_url_list[:-1],
                                            index=deep_base_url_list.index(conf['deepseek']['base_url']))
            model_1 = cols1[2].selectbox("model", deep_model_list[:-1],
                                         index=deep_model_list.index(conf['deepseek']['model']))
            max_tokens_1 = cols1[0].number_input("Deep最大输出Token:",
                                                 max_value=4096,
                                                 min_value=0,
                                                 value=int(conf['deepseek']['tokens']),
                                                 help="1个英文字符 ≈ 0.3 个 token。1 个中文字符 ≈ 0.6 个 token")
            temperature_1 = cols1[1].number_input("Deep模型随机性参数temperature:",
                                                  max_value=20,
                                                  min_value=0,
                                                  value=int(conf['deepseek']['temperature']),
                                                  help="模型随机性参数，数字越大，生成的结果随机性越大，一般为0.7，如果希望AI提供更多的想法，可以调大该数字")
            top_p_1 = cols1[2].number_input("Deep模型随机性参数top:",
                                            max_value=10,
                                            min_value=0,
                                            value=int(conf['deepseek']['top']),
                                            help="模型随机性参数，接近 1 时：模型几乎会考虑所有可能的词，只有概率极低的词才会被排除，随机性也越强；")

        st.subheader("通义千问模型配置【多角色：评审用例】")
        ai2 = st.checkbox("Qwen", eval(conf['qwen']['choice']))
        cols2 = st.columns([2, 2, 2])
        if ai2:
            api_key_2 = cols2[0].text_input("qwen_api_key",
                                            placeholder="sk-xxxxxxxxxxxxx",
                                            value=conf['qwen']['api_key'])
            base_url_2 = cols2[1].selectbox("base_url", qwen_base_url_list[:-1],
                                            index=qwen_base_url_list.index(conf['qwen']['base_url']))
            model_2 = cols2[2].selectbox("model", qwen_model_list[:-1],
                                         index=qwen_model_list.index(conf['qwen']['model']))
            max_tokens_2 = cols2[0].number_input("Qwen最大输出Token:",
                                                 max_value=4096,
                                                 min_value=0,
                                                 value=int(conf['qwen']['tokens']),
                                                 help="1个英文字符 ≈ 0.3 个 token。1 个中文字符 ≈ 0.6 个 token")
            temperature_2 = cols2[1].number_input("Qwen模型随机性参数temperature:",
                                                  max_value=20,
                                                  min_value=0,
                                                  value=int(conf['qwen']['temperature']),
                                                  help="模型随机性参数，数字越大，生成的结果随机性越大，一般为0.7，如果希望AI提供更多的想法，可以调大该数字")
            top_p_2 = cols2[2].number_input("Qwen模型随机性参数top:",
                                            max_value=10,
                                            min_value=0,
                                            value=int(conf['qwen']['top']),
                                            help="模型随机性参数，接近 1 时：模型几乎会考虑所有可能的词，只有概率极低的词才会被排除，随机性也越强；")

        if st.button('保存配置'):
            try:
                if ai1:
                    conf['deepseek'] = {
                        'choice': ai1,
                        'api_key': api_key_1,
                        'base_url': base_url_1,
                        'model': model_1,
                        'tokens': max_tokens_1,
                        'temperature': temperature_1,
                        'top': top_p_1,
                        'base_url_list': ",".join(deep_base_url_list),
                        'model_list': ",".join(deep_model_list)
                    }
                else:
                    conf['deepseek'] = {
                        'choice': ai1,
                        'api_key': conf['deepseek']['api_key'],
                        'base_url': conf['deepseek']['base_url'],
                        'model': conf['deepseek']['model'],
                        'tokens': conf['deepseek']['tokens'],
                        'temperature': conf['deepseek']['temperature'],
                        'top': conf['deepseek']['top'],
                        'base_url_list': conf['deepseek']['base_url_list'],
                        'model_list': conf['deepseek']['model_list']
                    }
                if ai2:
                    conf['qwen'] = {
                        'choice': ai2,
                        'api_key': api_key_2,
                        'base_url': base_url_2,
                        'model': model_2,
                        'tokens': max_tokens_2,
                        'temperature': temperature_2,
                        'top': top_p_2,
                        'base_url_list': ",".join(qwen_base_url_list),
                        'model_list': ",".join(qwen_model_list)
                    }
                else:
                    conf['qwen'] = {
                        'choice': ai2,
                        'api_key': conf['qwen']['api_key'],
                        'base_url': conf['qwen']['base_url'],
                        'model': conf['qwen']['model'],
                        'tokens': conf['qwen']['tokens'],
                        'temperature': conf['qwen']['temperature'],
                        'top': conf['qwen']['top'],
                        'base_url_list': conf['qwen']['base_url_list'],
                        'model_list': conf['qwen']['model_list']
                    }

                with open(config_path, 'w', encoding='utf-8') as f:
                    conf.write(f)
                with st.spinner('保存中...'):
                    time.sleep(1)
                st.balloons()
            except:
                st.error("【接口返回结果检查】输入数据只支持json格式数据")

    # AI交互
    with source_tab2:
        cases_rate_list = [60, 20, 20, 0, 0]
        cols3 = st.columns([2, 2])
        # 页面标题
        cols3[0].markdown("输入你的需求描述，AI 将为你生成相应的测试用例")
        # 高级选项（可折叠）
        with cols3[0].expander("高级选项"):
            show_slider = st.checkbox('用例分类占比(%)', True)
            cols4 = st.columns([2, 2])
            if show_slider:
                functional_testing = cols4[0].slider("功能用例", min_value=0, max_value=100, value=55)
                boundary_testing = cols4[0].slider("边界用例", min_value=0, max_value=100, value=25)
                exception_testing = cols4[0].slider("异常用例", min_value=0, max_value=100, value=20)
                perfmon_testing = cols4[1].slider("性能/兼容性用例", min_value=0, max_value=100, value=0)
                regression_testing = cols4[1].slider("回归测试用例", min_value=0, max_value=100, value=0)
                cases_rate_list = [functional_testing,
                                   boundary_testing,
                                   exception_testing,
                                   perfmon_testing,
                                   regression_testing]
            test_priority = st.selectbox("测试优先级", ["--", "急", "高", "中", "低"], index=0)
            # 添加测试用例数量控制
            test_case_count = st.number_input("生成测试用例数量",
                                              min_value=0,
                                              max_value=100,
                                              value=0,
                                              step=1,
                                              help="指定需要生成的测试用例数量")

        # 上传文件
        uploaded_file = cols3[0].file_uploader("上传需求", type=["txt"])
        uploaded_text = ""
        if uploaded_file is not None:
            uploaded_text = uploaded_file.read().decode('utf-8', 'ignore')

        # 用户输入区域
        user_input = cols3[0].text_area("需求描述",
                                        height=250,
                                        value=uploaded_text,
                                        placeholder="请详细描述你的功能需求，例如：\n"
                                                    "开发一个用户注册功能 \n"
                                                    "1、要求用户提供用户名、密码和电子邮件，\n"
                                                    "2、用户名长度为3-20个字符，\n"
                                                    "3、密码长度至少为8个字符且必须包含数字和字母，\n"
                                                    "4、电子邮件必须是有效格式。")

        system_writer_message = read_system_message("TESTCASE_WRITER_SYSTEM_MESSAGE.txt")
        system_reader_message = read_system_message("TESTCASE_READER_SYSTEM_MESSAGE.txt")
        tester_system_message = system_writer_message.replace("{{functional_testing}}", str(cases_rate_list[0]))\
            .replace("{{boundary_testing}}", str(cases_rate_list[1]))\
            .replace("{{exception_testing}}", str(cases_rate_list[2]))\
            .replace("{{perfmon_testing}}", str(cases_rate_list[3]))\
            .replace("{{regression_testing}}", str(cases_rate_list[4]))
        # 消息模板
        message_tab1, message_tab2 = cols3[1].tabs(["✍执行", "🔍 审核"])
        with message_tab1:
            customer_system_message = st.text_area("👉消息模板预览", height=480, value=tester_system_message)
        with message_tab2:
            customer_reader_message = st.text_area("👉消息模板预览", height=480, value=system_reader_message)
        # 调整模型参数
        model_deepseek_info["parameters"]["max_tokens"] = int(conf['deepseek']['tokens'])
        model_deepseek_info["parameters"]["temperature"] = int(conf['deepseek']['temperature']) / 10
        model_deepseek_info["parameters"]["top_p"] = int(conf['deepseek']['top']) / 10
        model_qwen_info["parameters"]["max_tokens"] = int(conf['qwen']['tokens'])
        model_qwen_info["parameters"]["temperature"] = int(conf['qwen']['temperature']) / 10
        model_qwen_info["parameters"]["top_p"] = int(conf['qwen']['top']) / 10

        # 提交按钮
        submit_button = cols3[0].button("生成测试用例")
        if submit_button:
            if bool(st.session_state.run_cases):
                st.session_state.update({"run_cases": False})
                # 处理提交
                if user_input:
                    # 准备任务描述
                    if test_priority != "--" and test_case_count != 0:
                        task = f""" 
                        需求描述: {user_input}
                        测试优先级: {test_priority}
                        【重要】请严格生成 {test_case_count} 条测试用例，不多不少。
                        """
                    elif test_case_count == 0 and test_priority != "--":
                        task = f""" 
                        需求描述: {user_input}
                        测试优先级: {test_priority}
                        """
                    elif test_case_count != 0 and test_priority == "--":
                        task = f""" 
                        需求描述: {user_input}
                        【重要】请严格生成 {test_case_count} 条测试用例，不多不少。
                        """
                    else:
                        task = f""" 
                        需求描述: {user_input}
                        """

                    # 创建一个固定的容器用于显示生成内容
                    response_container = st.container()

                    # 多角色参与生成用例
                    def m_roles_generate_testcases():
                        # 配置DeepSeek
                        deepseek_config = {
                            "config_list": [{
                                "model": conf['deepseek']['model'],
                                "base_url": conf['deepseek']['base_url'],
                                "api_key": conf['deepseek']['api_key'],
                                "stream": True  # DeepSeek模型要求启用流模式
                            }],
                            "temperature": float(conf['deepseek']['temperature']) / 10,
                            "max_tokens": int(conf['deepseek']['tokens'])
                        }
                        
                        # 配置Qwen
                        qwen_config = {
                            "config_list": [{
                                "model": conf['qwen']['model'],
                                "base_url": conf['qwen']['base_url'],
                                "api_key": conf['qwen']['api_key'],
                                "stream": True  # 启用流模式以保持一致性
                            }],
                            "temperature": float(conf['qwen']['temperature']) / 10,
                            "max_tokens": int(conf['qwen']['tokens'])
                        }
                        
                        # 创建代理
                        testcase_writer = get_testcase_writer(deepseek_config, customer_system_message)
                        testcase_reader = get_testcase_reader(qwen_config, customer_reader_message)
                        
                        # 创建用户代理
                        user_proxy = UserProxyAgent(
                            name="user_proxy",
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=0,
                            code_execution_config=False,
                        )
                        
                        # 创建一个空元素用于更新内容
                        with response_container:
                            placeholder = st.empty()
                            placeholder.text("正在生成测试用例...")
                        
                        # 首先让writer生成用例
                        writer_result = user_proxy.initiate_chat(
                            testcase_writer,
                            message=task,
                            max_turns=1,
                            silent=True
                        )
                        
                        # 获取writer的回复
                        writer_response = ""
                        if hasattr(testcase_writer, 'chat_messages'):
                            chat_messages = testcase_writer.chat_messages.get(user_proxy, [])
                            for msg in reversed(chat_messages):
                                if msg.get('role') == 'assistant':
                                    writer_response = msg.get('content', '')
                                    break
                        
                        # 让reader评审用例
                        reader_task = f"请评审以下测试用例：\n\n{writer_response}\n\n评审完成后，如果用例合格请回复'APPROVE'。"
                        reader_result = user_proxy.initiate_chat(
                            testcase_reader,
                            message=reader_task,
                            max_turns=1,
                            silent=True
                        )
                        
                        # 获取reader的回复
                        reader_response = ""
                        if hasattr(testcase_reader, 'chat_messages'):
                            chat_messages = testcase_reader.chat_messages.get(user_proxy, [])
                            for msg in reversed(chat_messages):
                                if msg.get('role') == 'assistant':
                                    reader_response = msg.get('content', '')
                                    break
                        
                        # 组合结果
                        full_response = f"{writer_response}\n\n--- 评审意见 ---\n{reader_response}"
                        
                        # 更新显示
                        with response_container:
                            placeholder.markdown(full_response)
                        
                        return full_response

                    # 单角色参与生成用例
                    def s_roles_generate_testcases():
                        # 配置DeepSeek
                        deepseek_config = {
                            "config_list": [{
                                "model": conf['deepseek']['model'],
                                "base_url": conf['deepseek']['base_url'],
                                "api_key": conf['deepseek']['api_key'],
                                "stream": True  # DeepSeek模型要求启用流模式
                            }],
                            "temperature": float(conf['deepseek']['temperature']) / 10,
                            "max_tokens": int(conf['deepseek']['tokens'])
                        }
                        
                        # 创建代理
                        testcase_writer = get_testcase_writer(deepseek_config, customer_system_message)
                        
                        # 创建用户代理
                        user_proxy = UserProxyAgent(
                            name="user_proxy",
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=0,
                            code_execution_config=False,
                        )
                        
                        # 创建一个空元素用于更新内容
                        with response_container:
                            placeholder = st.empty()
                            placeholder.text("正在生成测试用例...")
                        
                        # 生成用例
                        writer_result = user_proxy.initiate_chat(
                            testcase_writer,
                            message=task,
                            max_turns=1,
                            silent=True
                        )
                        
                        # 获取回复
                        full_response = ""
                        if hasattr(testcase_writer, 'chat_messages'):
                            chat_messages = testcase_writer.chat_messages.get(user_proxy, [])
                            for msg in reversed(chat_messages):
                                if msg.get('role') == 'assistant':
                                    full_response = msg.get('content', '')
                                    break
                        
                        # 更新显示
                        with response_container:
                            placeholder.markdown(full_response)
                        
                        return full_response

                    # 重新拉取消息
                    def show_message(message):
                        case_list_new = format_testcases(message)
                        with response_container:
                            placeholder = st.empty()
                            placeholder.markdown(message)
                            st.success("✅ 测试用例生成完成!")
                            st.download_button(
                                label="下载测试用例(.md)",
                                data="\n".join(case_list_new),
                                file_name="测试用例.md",
                                mime="text/markdown",
                                icon=":material/markdown:",
                            )

                            st.download_button(
                                label="下载测试用例(.xlsx)",
                                data=output.getvalue(),
                                file_name="测试用例.xlsx",
                                mime="application/vnd.ms-excel",
                                icon=":material/download:",
                            )

                    if eval(conf['deepseek']['choice']) and eval(conf['qwen']['choice']):
                        if conf['deepseek']['api_key'] != "" and conf['qwen']['api_key'] != "":
                            try:
                                with st.spinner("正在生成测试用例..."):
                                    result = m_roles_generate_testcases()
                                    case_list = format_testcases(result)
                                st.success("✅ 测试用例生成完成!")
                                if len(case_list):
                                    st.download_button(
                                        label="下载测试用例(.md)",
                                        data="\n".join(case_list),
                                        file_name="测试用例.md",
                                        mime="text/markdown",
                                        icon=":material/markdown:",
                                        on_click=show_message,
                                        args=(result,),
                                    )
                                    output = BytesIO()
                                    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                                    worksheet = workbook.add_worksheet()
                                    for row, case in enumerate(case_list):
                                        if case.find("--------") < 0:
                                            for col, cell in enumerate(case.split("|")):
                                                if col > 0:
                                                    if row > 1:
                                                        worksheet.write(row-1, col-1, str(cell).strip())
                                                    else:
                                                        worksheet.write(row, col-1, str(cell).strip())
                                    workbook.close()
                                    st.download_button(
                                        label="下载测试用例(.xlsx)",
                                        data=output.getvalue(),
                                        file_name="测试用例.xlsx",
                                        mime="application/vnd.ms-excel",
                                        icon=":material/download:",
                                        on_click=show_message,
                                        args=(result,),
                                    )
                            except Exception as e:
                                st.error(f"生成测试用例时出错: {str(e)}")
                        else:
                            st.error("请先配置DeepSeek/Qwen模型的APIKEY!")
                    elif eval(conf['deepseek']['choice']) and not eval(conf['qwen']['choice']):
                        if conf['deepseek']['api_key'] != "":
                            try:
                                with st.spinner("正在生成测试用例..."):
                                    result = s_roles_generate_testcases()
                                    case_list = format_testcases(result)
                                st.success("✅ 测试用例生成完成!")
                                if len(case_list):
                                    st.download_button(
                                        label="下载测试用例(.md)",
                                        data="\n".join(case_list),
                                        file_name="测试用例.md",
                                        mime="text/markdown",
                                        icon=":material/markdown:",
                                        on_click=show_message,
                                        args=(result,),
                                    )
                                    output = BytesIO()
                                    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
                                    worksheet = workbook.add_worksheet()
                                    for row, case in enumerate(case_list):
                                        if case.find("--------") < 0:
                                            for col, cell in enumerate(case.split("|")):
                                                if col > 0:
                                                    if row > 1:
                                                        worksheet.write(row - 1, col - 1, str(cell).strip())
                                                    else:
                                                        worksheet.write(row, col - 1, str(cell).strip())
                                    workbook.close()
                                    st.download_button(
                                        label="下载测试用例(.xlsx)",
                                        data=output.getvalue(),
                                        file_name="测试用例.xlsx",
                                        mime="application/vnd.ms-excel",
                                        icon=":material/download:",
                                        on_click=show_message,
                                        args=(result,),
                                    )
                            except Exception as e:
                                st.error(f"生成测试用例时出错: {str(e)}")
                        else:
                            st.error("请先配置DeepSeek模型的APIKEY!")
                    else:
                        st.error("请先配置DeepSeek模型并选中保存!")
                    st.session_state.update({"run_cases": True})

                elif submit_button and not user_input:
                    st.error("请输入需求描述")
                    st.session_state.update({"run_cases": True})
            else:
                st.warning("正在生成测试用例中，请不要频繁操作！")
    return None


if __name__ == '__main__':
    main()
