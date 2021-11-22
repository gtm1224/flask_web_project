from flask import request, redirect, url_for, render_template
from libs import db
from models import Article,Category
from flask import Blueprint

article_app = Blueprint("article_app",__name__)

@article_app.route("/post",methods=['get','post'])
def post():
    if request.method == "POST":
        cate_id = request.form['cate']
        title = request.form['title']
        intro = request.form['intro']
        content = request.form['content']
        article = Article(
            title = title,
            intro = intro,
            content = content,
            author = "Tim",
            cate_id=cate_id
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for(".list"))
    return render_template("article/post.html")

# 获得文章列表
@article_app.route("/list/<int:page>", methods=['get', "post"])
@article_app.route("/list", defaults={"page":1},methods=['get', "post"])
def list(page):
    if request.method == "POST":
        q = request.form['q']
        condition = {request.form['field']:q}
        if request.form['field'] == "title":
            condition = Article.title.like('%%%s%%' % q)
        else:
            condition = Article.content.like('%%%s%%' % q)
        if request.form['order'] == "1":
            order = Article.id.asc()
        else:
            order = Article.id.desc()

        res = Article.query.filter(condition)\
                                .order_by(order)\
                                .paginate(page, 10)


    else:
        res = Article.query.paginate(page,10)

    # 无论搜索还是默认查看，都是翻页处理
    articles = res.items
    pageList = res.iter_pages()


    return render_template("article/article_list.html", articles=articles,
                           pageList=pageList
                           )



# 根据文章id删除文章
@article_app.route("/delete/<int:article_id>")
def delete(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for(".list"))

# 文章修改
@article_app.route("/edit/<int:article_id>",methods=['get','post'])
def edit(article_id):
    article = Article.query.get(article_id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.content = request.form['content']
        db.session.commit()
        return redirect(url_for(".list"))
    return render_template("article/edit_article.html",article=article)

# 根据文章id阅读文章
@article_app.route("/view/<int:article_id>")
def view(article_id):
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for(".list"))
    return render_template("article/detail.html",article=article)

# 根据文章cate_id显示文章列表
@article_app.route("/cate/<int:cate_id>/<int:page>")
@article_app.route("/",defaults={"cate_id":0,"page":1})
def getArticleList(cate_id,page):
    if cate_id == 0:
        res = Article.query.paginate(page,20)
    else:
        res = Article.query.filter_by(cate_id=cate_id).paginate(page,20)
    articles = res.items
    pageList = res.iter_pages()
    return render_template("index.html",articles = articles,pageList=pageList)

# 分类视图部分
# 添加分类
@article_app.route("/add_cate", methods=['get','post'])
def addCate():
    message = None
    if request.method == "POST":
        cate_name = request.form['name']
        cate_order    = request.form['order']
        category = Category(
                    cate_name=cate_name,
                    cate_order=cate_order,
         )
        try:
            db.session.add(category)
            db.session.commit()
            message = cate_name+"添加成功"
        except Exception as e:
            message = "发生了错误:" + str(e)
            # 如果插入失败，进行回滚操作
            db.session.rollback()

    return render_template("category/add.html", message=message)


# 获得分类列表
@article_app.route("/cate_list")
def cateList():

    cates = Category.query.order_by(Category.cate_order.desc()).all()
    return render_template("category/list.html", cates=cates )


# 删除分类
@article_app.route("/cate_delete/<int:cate_id>")
def deleteCate(cate_id):
    cate = Category.query.get(cate_id)
    db.session.delete(cate)
    db.session.commit()
    return redirect(url_for(".cateList"))


# 分类修改
@article_app.route("/cate_edit/<int:cate_id>", methods=['get', 'post'])
def editCate(cate_id):
    category = Category.query.get(cate_id)
    if request.method == "POST":
        category.cate_name = request.form['name']
        category.cate_order = request.form['order']
        db.session.commit()
        return redirect(url_for(".cateList"))
    return render_template("category/edit.html", category=category)