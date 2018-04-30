from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import BlogsForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://news:password@localhost/blogs?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'a random string'
db = SQLAlchemy(app)


class Blogs(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    types = db.Column(db.Enum('系统', '软件', '杂谈'))
    images = db.Column(db.String(120))
    author = db.Column(db.String(120))
    view_count = db.Column(db.Integer)
    is_valid = db.Column(db.Boolean)
    create_time = db.Column(db.String(120))
    update_time = db.Column(db.String(120))

    # 打印博客标题
    def __repr__(self):
        return '<Blogs %r>' % self.title


@app.route('/')
def index():
    """ 博客主页 """
    blogs_list = Blogs.query.filter_by(is_valid=1)
    return render_template('index.html', blogs_list=blogs_list)


@app.route('/cat/<name>/')
def cat(name):
    blogs_list = Blogs.query.filter_by(is_valid=1, types=name)
    return render_template('cat.html', name=name, blogs_list=blogs_list)


@app.route('/detail/<int:pk>/')
def detail(pk):
    new_obj = Blogs.query.get(pk)
    return render_template('detail.html', new_obj=new_obj, pk=pk)


@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
    if page is None:
        page = 1
    page_data = Blogs.query.filter_by(is_valid=1).paginate(page=page, per_page=4)
    return render_template('/admin/index.html', page_data=page_data)


@app.route('/admin/add/', methods=['GET', 'POST'])
def add():
    """ 新增文章 """
    form = BlogsForm()
    if form.validate_on_submit():
        blog = Blogs(
            title=form.title.data,
            content=form.content.data,
            types=form.types.data,
            images=form.images.data,
            is_valid=True,
            create_time=datetime.now(),
            update_time=datetime.now(),
            )
        db.session.add(blog)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('admin'))
    return render_template('/admin/add.html', form=form)


@app.route('/admin/delete/<int:pk>/', methods=['POST'])
def delete(pk):
    """ 删除文章，限定通过get访问无法操作 """
    if request.method == "POST":
        obj = Blogs.query.get(pk)
        if not obj:
            return False
        obj.is_valid = False
        flash('已删除')
        db.session.add(obj)
        db.session.commit()
        return '删除成功'
    return False


@app.route('/admin/update/<int:pk>', methods=['GET', 'POST'])
def update(pk):
    """ 更新文章 """
    obj = Blogs.query.get(pk)
    if obj is None:
        abort(404)
    form = BlogsForm(obj=obj)
    if form.validate_on_submit():
        blog = Blogs(
            title=form.title.data,
            content=form.content.data,
            types=form.types.data,
            images=form.images.data,
            update_time=datetime.now(),
            )
        db.session.add(blog)
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('admin'))
    return render_template('/admin/update.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()
