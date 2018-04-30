from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class BlogsForm(FlaskForm):
    """ 博客表单 """
    title = StringField(label='标题', validators=[DataRequired("请输入标题")],
                        description="请输入标题",
                        render_kw={"required": "required", "class": "form-control"})
    content = TextAreaField(label='正文', validators=[DataRequired("请输入内容")],
                            description="请输入内容",
                            render_kw={"required": "required", "class": "form-control"})
    types = SelectField('分类', choices=[('系统', '系统'), ('软件', '软件'), ('杂谈', '杂谈')],
                        render_kw={'class': 'form-control'})
    images = StringField(label='图片', description='请输入图片地址',
                         render_kw={'required': 'required', 'class': 'form-control'})
    submit = SubmitField('提交')
