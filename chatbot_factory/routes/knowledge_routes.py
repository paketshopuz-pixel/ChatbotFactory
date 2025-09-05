# chatbot_factory/routes/knowledge_routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from flask_babel import gettext as _
from .. import db
from ..models import Bot, KnowledgeBase, Product
from ..forms import KnowledgeBaseForm, ProductForm

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route("/bot/<int:bot_id>/knowledge", methods=['GET'])
@login_required
def manage_knowledge(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    
    text_form = KnowledgeBaseForm()
    entries = bot.knowledge_base
    products = bot.products
    return render_template('knowledge_base.html', title=_('Knowledge Base'), bot=bot, 
                           text_form=text_form, entries=entries, products=products)

@knowledge_bp.route("/bot/<int:bot_id>/knowledge/add_text", methods=['POST'])
@login_required
def add_text_entry(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    form = KnowledgeBaseForm()
    if form.validate_on_submit():
        entry = KnowledgeBase(title=form.title.data, content=form.content.data, bot=bot)
        db.session.add(entry)
        db.session.commit()
        flash(_('New text entry has been added!'), 'success')
    return redirect(url_for('knowledge.manage_knowledge', bot_id=bot_id))

@knowledge_bp.route("/bot/<int:bot_id>/add_product", methods=['GET', 'POST'])
@login_required
def add_product(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(bot_id=bot.id, name=form.name.data, price=form.price.data, 
                          description=form.description.data, image_url=form.image_url.data)
        db.session.add(product)
        db.session.commit()
        flash(_('New product has been added to the knowledge base!'), 'success')
        return redirect(url_for('knowledge.manage_knowledge', bot_id=bot.id))
    return render_template('add_product.html', title=_('Add Product'), form=form, bot=bot)

@knowledge_bp.route("/knowledge/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_knowledge(entry_id):
    # Bu funksiya o'zgarishsiz qoladi
    entry = KnowledgeBase.query.get_or_404(entry_id)
    bot = entry.bot
    if bot.owner != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash(_('The text entry has been deleted.'), 'success')
    return redirect(url_for('knowledge.manage_knowledge', bot_id=bot.id))

@knowledge_bp.route("/product/<int:product_id>/delete", methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    bot = product.bot_owner
    if bot.owner != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash(_('The product has been deleted.'), 'success')
    return redirect(url_for('knowledge.manage_knowledge', bot_id=bot.id))