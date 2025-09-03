from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import db, Ticket, User
from app.forms import TicketForm, UpdateTicketForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data,
                        priority=form.priority.data, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted successfully!')
        return redirect(url_for('main.my_tickets'))
    return render_template('submit_ticket.html', form=form)

@main.route('/my_tickets')
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('my_tickets.html', tickets=tickets)

@main.route('/all_tickets')
@login_required
def all_tickets():
    if current_user.role != 'support':
        flash('Access denied')
        return redirect(url_for('main.index'))
    tickets = Ticket.query.all()
    return render_template('all_tickets.html', tickets=tickets)

@main.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    if current_user.role != 'support' and ticket.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('main.index'))
    form = UpdateTicketForm()
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.filter_by(role='support').all()]
    if form.validate_on_submit() and current_user.role == 'support':
        ticket.status = form.status.data
        ticket.assigned_to = form.assigned_to.data
        db.session.commit()
        flash('Ticket updated!')
        return redirect(url_for('main.ticket_detail', id=id))
    return render_template('ticket_detail.html', ticket=ticket, form=form)
