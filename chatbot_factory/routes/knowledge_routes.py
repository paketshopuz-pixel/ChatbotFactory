# chatbot_factory/routes/knowledge_routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from flask_babel import gettext as _
from .. import db
from ..models import Bot, KnowledgeBase
from ..forms import KnowledgeBaseForm

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route("/bot/<int:bot_id>/knowledge", methods=['GET', 'POST'])
@login_required
def manage_knowledge(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    
    form = KnowledgeBaseForm()
    if form.validate_on_submit():
        entry = KnowledgeBase(title=form.title.data, content=form.content.data, bot=bot)
        db.session.add(entry)
        db.session.commit()
        flash(_('New knowledge base entry has been added!'), 'success')
        return redirect(url_for('knowledge.manage_knowledge', bot_id=bot.id))
    
    entries = bot.knowledge_base
    return render_template('knowledge_base.html', title=_('Knowledge Base'), bot=bot, form=form, entries=entries)

@knowledge_bp.route("/knowledge/<int:entry_id>/delete", methods=['POST'])
@login_required
def delete_knowledge(entry_id):
    entry = KnowledgeBase.query.get_or_404(entry_id)
    bot = entry.bot
    if bot.owner != current_user:
        abort(403)
    
    db.session.delete(entry)
    db.session.commit()
    flash(_('The entry has been deleted.'), 'success')
    return redirect(url_for('knowledge.manage_knowledge', bot_id=bot.id))