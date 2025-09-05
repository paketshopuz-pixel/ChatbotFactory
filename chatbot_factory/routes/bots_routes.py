# chatbot_factory/routes/bots_routes.py
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from flask_babel import gettext as _
from chatbot_factory import db
from chatbot_factory.models import Bot
from chatbot_factory.forms import BotForm

bots_bp = Blueprint('bots', __name__)

@bots_bp.route("/bot/create", methods=['GET', 'POST'])
@login_required
def create_bot():
    # --- YANGI TEKSHIRUV KODI ---
    bot_count = Bot.query.filter_by(owner=current_user).count()
    if bot_count >= current_user.subscription.max_bots:
        flash(_('You have reached the maximum number of bots for your current plan. Please upgrade to create more.'), 'warning')
        return redirect(url_for('auth.dashboard'))
    # --- TEKSHIRUV KODI TUGADI ---

    form = BotForm()
    if form.validate_on_submit():
        bot = Bot(name=form.name.data, platform_type=form.platform_type.data,
                  telegram_token=form.telegram_token.data, owner=current_user)
        db.session.add(bot)
        db.session.commit()
        flash(_('Your new bot has been created!'), 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('bot_form.html', title=_('Create Bot'), form=form, legend=_('New Bot'))

@bots_bp.route("/bot/<int:bot_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_bot(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    form = BotForm()
    if form.validate_on_submit():
        bot.name = form.name.data
        bot.platform_type = form.platform_type.data
        bot.telegram_token = form.telegram_token.data
        db.session.commit()
        flash(_('Your bot has been updated!'), 'success')
        return redirect(url_for('auth.dashboard'))
    elif request.method == 'GET':
        form.name.data = bot.name
        form.platform_type.data = bot.platform_type.name
        form.telegram_token.data = bot.telegram_token
    return render_template('bot_form.html', title=_('Edit Bot'), form=form, legend=_('Edit Bot'))

@bots_bp.route("/bot/<int:bot_id>/delete", methods=['POST'])
@login_required
def delete_bot(bot_id):
    bot = Bot.query.get_or_404(bot_id)
    if bot.owner != current_user:
        abort(403)
    db.session.delete(bot)
    db.session.commit()
    flash(_('Your bot has been deleted!'), 'success')
    return redirect(url_for('auth.dashboard'))