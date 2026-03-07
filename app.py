from flask import Flask, render_template, request
import ai_utils
import markdown  # 新增导入

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    requirement = request.form['requirement']
    if not requirement:
        return "请输入需求描述"
    result_md = ai_utils.generate_testcases(requirement)  # 这是 Markdown 原文

    # 将 Markdown 转换为 HTML（启用表格扩展）
    result_html = markdown.markdown(result_md, extensions=['tables'])

    # 将转换后的 HTML 传递给模板
    return render_template('index.html', result=result_html, requirement=requirement)


@app.route('/defect')
def defect_page():
    return render_template('defect.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    defect = request.form['defect']
    if not defect:
        return "请输入缺陷描述"
    result_md = ai_utils.analyze_defect(defect)

    # 同样转换缺陷分析结果（可能也包含 Markdown 格式）
    result_html = markdown.markdown(result_md, extensions=['tables'])

    return render_template('defect.html', result=result_html, defect=defect)


if __name__ == '__main__':
    app.run(debug=True)