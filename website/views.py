from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for,flash
from flask_login import login_required, current_user
from .models import Product, UserSession, User, ManDay, Planned, Info, Contact, Stock
from . import db
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def main():
    email = current_user.email
    if current_user.rid == 'team':
        return render_template('home.html', email = email)
    else:
         return render_template('no.html', email = email)



@views.route('/gantt')
@login_required
def gantt():
    return render_template('soon.html')

@views.route('/pmt')
@login_required
def index():
    # Check if an entry already exists for the current user
    existing_info = Info.query.filter_by(user_id=current_user.id).first()

    if not existing_info:
        new_info = Info(
            loc='',
            po=1,
            pon='',
            rev=1,
            iof=1,
            revdate='',
            iofdate = '',
            iof1=1,
            iof2='',
            user_id=current_user.id
        )
        db.session.add(new_info)
        db.session.commit()


    products = Product.query.filter_by(user_id=current_user.id).all()
    infos = Info.query.filter_by(user_id=current_user.id).all()
    email = current_user.email

    return render_template('index.html', products=products,email = email, infos = infos)


@views.route('/add_product', methods=['POST'])
@login_required
def add_product():
    part_nos = request.form.getlist('partNo[]')
    categories = request.form.getlist('category[]')
    makes = request.form.getlist('make[]')
    qtys = request.form.getlist('qty[]')
    approved_not_approveds = request.form.getlist('approvedNotapproved[]')
    billable_non_billables = request.form.getlist('billableNonBillable[]')
    ordered_qtys = request.form.getlist('orderedqty[]')
    order_statuses = request.form.getlist('orderStatus[]')
    podates = request.form.getlist('podate[]')
    delivery_periods = request.form.getlist('deliveryPeriod[]')
    delivery_ats = request.form.getlist('deliveryAt[]')
    supplied_qtys = request.form.getlist('suppliedQty[]')
    delivery_statuses = request.form.getlist('deliveryStatus[]')
    backlog_qtys = request.form.getlist('backlogQty[]')
    remarks_list = request.form.getlist('remarks[]')

    loc = request.form['loc'] if request.form['loc'] else ''
    po = int(request.form['po']) if request.form['po'] else 1
    pon = (request.form['pon']) if request.form['pon'] else ''
    rev = int(request.form['rev']) if request.form['rev'] else 1
    iof = int(request.form['iof']) if request.form['iof'] else 1
    revdate = (request.form['revdate']) if request.form['revdate'] else ''
    iofdate = (request.form['iofdate']) if request.form['iofdate'] else ''
    iof1 = int(request.form['iof1']) if request.form['iof1'] else 1
    iof2 =  (request.form['iof2']) if request.form['iof2'] else ''

    new_info = Info(
                loc = loc,
                po = po, pon = pon,
                rev = rev,
                iof = iof,
                revdate = revdate,
                iofdate = iofdate,
                iof1 = iof1,
                iof2 = iof2,
                user_id=current_user.id
            )

    db.session.add(new_info)


    for i in range(len(part_nos)):
        part_no = part_nos[i]
        existing_product = Product.query.filter_by(part_no=part_no, user_id=current_user.id).first()

        if existing_product:
            # Update existing product
            existing_product.category = categories[i]
            existing_product.make = makes[i]
            existing_product.qty = int(qtys[i]) if qtys[i] else 0
            existing_product.approved_not_approved = approved_not_approveds[i]
            existing_product.billable_non_billable = billable_non_billables[i]
            existing_product.ordered_qty = int(ordered_qtys[i]) if ordered_qtys[i] else 0
            existing_product.order_status = order_statuses[i]
            existing_product.podate = podates[i]
            existing_product.delivery_period = delivery_periods[i]
            existing_product.delivery_at = delivery_ats[i]
            existing_product.supplied_qty = int(supplied_qtys[i]) if supplied_qtys[i] else 0
            existing_product.delivery_status = delivery_statuses[i]
            existing_product.backlog_qty = int(backlog_qtys[i]) if backlog_qtys[i] else 0
            existing_product.remarks = remarks_list[i]
        else:
            # Create new product

            new_product = Product(
                part_no=part_no,
                category=categories[i],
                make=makes[i],
                qty=int(qtys[i]) if qtys[i] else 0,
                approved_not_approved=approved_not_approveds[i],
                billable_non_billable=billable_non_billables[i],
                ordered_qty=int(ordered_qtys[i]) if ordered_qtys[i] else 0,
                order_status=order_statuses[i],
                podate=podates[i],
                delivery_period=delivery_periods[i],
                delivery_at=delivery_ats[i],
                supplied_qty=int(supplied_qtys[i]) if supplied_qtys[i] else 0,
                delivery_status=delivery_statuses[i],
                backlog_qty=int(backlog_qtys[i]) if backlog_qtys[i] else 0,
                remarks=remarks_list[i],
                user_id=current_user.id

            )
            db.session.add(new_product)

    db.session.commit()


    return redirect(url_for('views.display'))



@views.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of exception
        return jsonify({'status': 'error', 'message': str(e)}), 500

@views.route('/delete_product_ppt/<int:id>', methods=['DELETE'])
def delete_product_ppt(id):
    try:
        record = ManDay.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of exception
        return jsonify({'status': 'error', 'message': str(e)}), 500



@views.route('/display')
@login_required
def display():

    infos = Info.query.filter_by(user_id=current_user.id).all()
    email = current_user.email
    products = Product.query.filter_by(user_id=current_user.id).all()

    pr = Product.query.filter(Product.user_id == current_user.id, Product.remarks.isnot('')).all()

    total_parts = len(products)
    approved_tds = sum(1 for product in products if product.approved_not_approved == 'approved')
    not_approved_tds = total_parts - approved_tds
    pending_orders = sum(1 for product in products if product.order_status == 'pending')
    confirmed_orders = sum(1 for product in products if product.order_status == 'confirmed')
    cancelled_orders = sum(1 for product in products if product.order_status == 'cancelled')
    pending_deliveries = sum(1 for product in products if product.delivery_status == 'pending')
    partiallypending_deliveries = sum(1 for product in products if product.delivery_status == 'partiallypending')
    completed_deliveries = sum(1 for product in products if product.delivery_status == 'completed')
    delayed_deliveries = sum(1 for product in products if product.delivery_status == 'delayed')
    current_date = datetime.now().strftime('%d-%m-%Y')


    return render_template('display.html',
                           products=products,infos = infos, pr = pr,
                           total_parts=total_parts,
                           approved_tds=approved_tds,
                           not_approved_tds=not_approved_tds,
                           pending_orders=pending_orders,
                           confirmed_orders=confirmed_orders,
                           cancelled_orders=cancelled_orders,
                           pending_deliveries=pending_deliveries,
                           partiallypending_deliveries=partiallypending_deliveries,
                           completed_deliveries=completed_deliveries,
                           delayed_deliveries=delayed_deliveries, email=email,current_date = current_date)



@views.route('/all', methods=['GET'])
def all():
    try:
        emails = [user.email for user in User.query.all()]  # Fetch all emails from the database
        return render_template('all.html', emails=emails)
    except Exception as e:
        return str(e)


@views.route('/ppt')
def ppt():
    # Fetch mandays data filtered by user_id and uniquee
    manday = (
        db.session.query(ManDay)
        .filter(ManDay.user_id == current_user.id)
        .group_by(ManDay.uniquee)  # Group by uniquee to get distinct values
        .all()
    )
    planned = db.session.query(Planned).filter(Planned.user_id == current_user.id).first()
    contact = db.session.query(Contact).filter(Contact.user_id == current_user.id).first()
    email = current_user.email

    user_type = current_user.p_type  # Get the user's type

    # Render the appropriate template based on user type
    if user_type == 'FAS1':
        return render_template('FAS1.html', manday=manday, planned=planned, email=email, contact=contact)
    elif user_type == 'FAS2':
        return render_template('FAS1.html', manday=manday, planned=planned, email=email, contact=contact)
    elif user_type == 'FAS+PA1':
        return render_template('FAS+PA1.html', manday=manday, planned=planned, email=email, contact=contact)
    elif user_type == 'FAS+PA2':
        return render_template('FAS+PA1.html', manday=manday, planned=planned, email=email, contact=contact)
    elif user_type == 'FAS+PA+TWTB1':
        return render_template('ppt.html', manday=manday, planned=planned, email=email, contact=contact)
    elif user_type == 'FAS+PA+TWTB2':
        return render_template('ppt.html', manday=manday, planned=planned, email=email, contact=contact)
    else:
        # Default template or handle unexpected user types
        return render_template('default.html', manday=manday, planned=planned, email=email, contact=contact)


@views.route('/output')
@login_required
def output():
    mandays = (
        db.session.query(ManDay)
        .filter(ManDay.user_id == current_user.id)
        .group_by(ManDay.uniquee)
        .all()
    )
    rec = ManDay.query.filter(ManDay.user_id == current_user.id, ManDay.remarks.isnot('')).all()

    planned = db.session.query(Planned).filter(Planned.user_id == current_user.id).first()

    contact = db.session.query(Contact).filter(Contact.user_id == current_user.id).first()
    products = Product.query.filter_by(user_id=current_user.id).all()
    infos = db.session.query(Info).filter(Info.user_id == current_user.id).all()
    current_date = datetime.now().strftime('%d-%m-%Y')


    # Sum the actual values from the mandays records
    cable_actual = sum(manday.cable for manday in mandays if manday.cable)
    pvc_actual = sum(manday.pvc for manday in mandays if manday.pvc)
    mark_actual = sum(manday.markingdrilling for manday in mandays if manday.markingdrilling)
    ci_actual = sum(manday.ci for manday in mandays if manday.ci)
    
    pvc_actual1 = sum(manday.pvc1 for manday in mandays if manday.pvc1)
    mark_actual1 = sum(manday.markingdrilling1 for manday in mandays if manday.markingdrilling1)
    ci_actual1 = sum(manday.ci1 for manday in mandays if manday.ci1)
    cable_actual2 = sum(manday.cable2 for manday in mandays if manday.cable2)
    pvc_actual2 = sum(manday.pvc2 for manday in mandays if manday.pvc2)
    mark_actual2 = sum(manday.markingdrilling2 for manday in mandays if manday.markingdrilling2)
    ci_actual2 = sum(manday.ci2 for manday in mandays if manday.ci2)
    backboxinstallation_actual = sum(manday.backboxinstallation for manday in mandays if manday.backboxinstallation)
    baseinstallation_actual = sum(manday.baseinstallation for manday in mandays if manday.baseinstallation)
    detectorinstallation_actual = sum(manday.detectorinstallation for manday in mandays if manday.detectorinstallation)
    controlmoduleinstallation_actual = sum(manday.controlmoduleinstallation for manday in mandays if manday.controlmoduleinstallation)
    hooterinstallation_actual = sum(manday.hooterinstallation for manday in mandays if manday.hooterinstallation)
    mcpinstallation_actual = sum(manday.mcpinstallation for manday in mandays if manday.mcpinstallation)
    responseindicatorinstallation_actual = sum(manday.responseindicatorinstallation for manday in mandays if manday.responseindicatorinstallation)
    monitormoduleinstallation_actual = sum(manday.monitormoduleinstallation for manday in mandays if manday.monitormoduleinstallation)
    controlrelaymoduleinstallation_actual = sum(manday.controlrelaymoduleinstallation for manday in mandays if manday.controlrelaymoduleinstallation)
    isolatormoduleinstallation_actual = sum(manday.isolatormoduleinstallation for manday in mandays if manday.isolatormoduleinstallation)
    paspeakerinstallation_actual = sum(manday.paspeakerinstallation for manday in mandays if manday.paspeakerinstallation)
    twtbbackboxinstallation_actual = sum(manday.twtbbackboxinstallation for manday in mandays if manday.twtbbackboxinstallation)
    twtbspeakerinstallation_actual = sum(manday.twtbspeakerinstallation for manday in mandays if manday.twtbspeakerinstallation)
    firepanelinstallation_actual = sum(manday.firepanelinstallation for manday in mandays if manday.firepanelinstallation)
    pacontrollerinstallation_actual = sum(manday.pacontrollerinstallation for manday in mandays if manday.pacontrollerinstallation)
    twtbcontrollerinstallation_actual = sum(manday.twtbcontrollerinstallation for manday in mandays if manday.twtbcontrollerinstallation)
    smpsinstallation_actual = sum(manday.smpsinstallation for manday in mandays if manday.smpsinstallation)
    detectortesting_actual = sum(manday.detectortesting for manday in mandays if manday.detectortesting)
    continuitytesting_actual = sum(manday.continuitytesting for manday in mandays if manday.continuitytesting)
    programming_actual = sum(manday.programming for manday in mandays if manday.programming)
    continuitytesting_actual1 = sum(manday.continuitytesting1 for manday in mandays if manday.continuitytesting1)
    programming_actual1 = sum(manday.programming1 for manday in mandays if manday.programming1)
    continuitytesting_actual2 = sum(manday.continuitytesting2 for manday in mandays if manday.continuitytesting2)
    programming_actual2 = sum(manday.programming2 for manday in mandays if manday.programming2)
    chippingplasting_actual = sum(manday.chippingplasting for manday in mandays if manday.chippingplasting)
    handingoverdocument_actual = sum(manday.handingoverdocument for manday in mandays if manday.handingoverdocument)
    user_type = current_user.p_type
    if user_type == 'FAS+PA+TWTB1':
        return render_template(
        'output.html', products = products, infos = infos,current_date = current_date,
        records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        pvc_actual1=pvc_actual1,
        mark_actual1=mark_actual1,
        ci_actual1=ci_actual1,
        cable_actual2=cable_actual2,
        pvc_actual2=pvc_actual2,
        mark_actual2=mark_actual2,
        ci_actual2=ci_actual2,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        paspeakerinstallation_actual=paspeakerinstallation_actual,
        twtbbackboxinstallation_actual=twtbbackboxinstallation_actual,
        twtbspeakerinstallation_actual=twtbspeakerinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        pacontrollerinstallation_actual=pacontrollerinstallation_actual,
        twtbcontrollerinstallation_actual=twtbcontrollerinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        continuitytesting_actual1=continuitytesting_actual1,
        programming_actual1=programming_actual1,
        continuitytesting_actual2=continuitytesting_actual2,
        programming_actual2=programming_actual2,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
    )
    elif user_type == 'FAS+PA+TWTB2':
        return render_template(
        'output1.html', products = products, infos = infos,current_date = current_date,
        records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        pvc_actual1=pvc_actual1,
        mark_actual1=mark_actual1,
        ci_actual1=ci_actual1,
        cable_actual2=cable_actual2,
        pvc_actual2=pvc_actual2,
        mark_actual2=mark_actual2,
        ci_actual2=ci_actual2,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        paspeakerinstallation_actual=paspeakerinstallation_actual,
        twtbbackboxinstallation_actual=twtbbackboxinstallation_actual,
        twtbspeakerinstallation_actual=twtbspeakerinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        pacontrollerinstallation_actual=pacontrollerinstallation_actual,
        twtbcontrollerinstallation_actual=twtbcontrollerinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        continuitytesting_actual1=continuitytesting_actual1,
        programming_actual1=programming_actual1,
        continuitytesting_actual2=continuitytesting_actual2,
        programming_actual2=programming_actual2,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
    )



@views.route('/save_data', methods=['POST'])
@login_required
def save_data():
    try:
        # Extract form data from POST request
        uniquees = request.form.getlist('uniquee[]')
        days = request.form.getlist('day[]')
        dates = request.form.getlist('date[]')
        sdates = request.form.getlist('sdate[]')
        sites = request.form.getlist('site[]')
        subs = request.form.getlist('sub[]')
        remarks_list = request.form.getlist('remarks[]')
        supports = request.form.getlist('support[]')
        support1s = request.form.getlist('support1[]')
        cables = request.form.getlist('cable[]')
        pvcs = request.form.getlist('pvc[]')
        markingDrillings = request.form.getlist('markingdrilling[]')
        cis = request.form.getlist('ci[]')
        pvcs1= request.form.getlist('pvc1[]')
        markingDrillings1 = request.form.getlist('markingdrilling1[]')
        cis1 = request.form.getlist('ci1[]')
        
        pvcs2 = request.form.getlist('pvc2[]')
        markingDrillings2 = request.form.getlist('markingdrilling2[]')
        cis2 = request.form.getlist('ci2[]')
        backboxInstallations = request.form.getlist('backboxinstallation[]')
        baseInstallations = request.form.getlist('baseinstallation[]')
        detectorInstallations = request.form.getlist('detectorinstallation[]')
        controlModuleInstallations = request.form.getlist('controlmoduleinstallation[]')
        hooterInstallations = request.form.getlist('hooterinstallation[]')
        mcpInstallations = request.form.getlist('mcpinstallation[]')
        responseIndicatorInstallations = request.form.getlist('responseindicatorinstallation[]')
        monitorModuleInstallations = request.form.getlist('monitormoduleinstallation[]')
        controlRelayModuleInstallations = request.form.getlist('controlrelaymoduleinstallation[]')
        isolatorModuleInstallations = request.form.getlist('isolatormoduleinstallation[]')
        paSpeakerInstallations = request.form.getlist('paspeakerinstallation[]')
        twtbBackboxInstallations = request.form.getlist('twtbbackboxinstallation[]')
        twtbSpeakerInstallations = request.form.getlist('twtbspeakerinstallation[]')
        firePanelInstallations = request.form.getlist('firepanelinstallation[]')
        paControllerInstallations = request.form.getlist('pacontrollerinstallation[]')
        twtbControllerInstallations = request.form.getlist('twtbcontrollerinstallation[]')
        smpsInstallations = request.form.getlist('smpsinstallation[]')
        detectorTestings = request.form.getlist('detectortesting[]')
        continuityTestings = request.form.getlist('continuitytesting[]')
        programmings = request.form.getlist('programming[]')
        continuityTestings1 = request.form.getlist('continuitytesting1[]')
        programmings1 = request.form.getlist('programming1[]')
        continuityTestings2 = request.form.getlist('continuitytesting2[]')
        programmings2 = request.form.getlist('programming2[]')
        chippingPlastings = request.form.getlist('chippingplasting[]')
        handingOverDocuments = request.form.getlist('handingoverdocument[]')

        # Contact details
        name1 = request.form['name1'] if request.form['name1'] else ''
        name2 = request.form['name2'] if request.form['name2'] else ''
        email1 = request.form['email1'] if request.form['email1'] else ''
        email2 = request.form['email2'] if request.form['email2'] else ''
        contact1 = int(request.form['contact1']) if request.form['contact1'] else 0
        contact2 = int(request.form['contact2']) if request.form['contact2'] else 0

        # Planned data
        start = request.form['start'] if request.form['start'] else ''
        cable_planned = int(request.form['cable_planned']) if request.form['cable_planned'] else 1
        pvc_planned = int(request.form['pvc_planned']) if request.form['pvc_planned'] else 1
        mark_planned = int(request.form['mark_planned']) if request.form['mark_planned'] else 1
        ci_planned = int(request.form['ci_planned']) if request.form['ci_planned'] else 1
        pvc_planned1 = int(request.form['pvc_planned1']) if request.form['pvc_planned1'] else 1
        mark_planned1 = int(request.form['mark_planned1']) if request.form['mark_planned1'] else 1
        ci_planned1 = int(request.form['ci_planned1']) if request.form['ci_planned1'] else 1
        cable_planned2 = int(request.form['cable_planned2']) if request.form['cable_planned2'] else 1
        pvc_planned2 = int(request.form['pvc_planned2']) if request.form['pvc_planned2'] else 1
        mark_planned2 = int(request.form['mark_planned2']) if request.form['mark_planned2'] else 1
        ci_planned2 = int(request.form['ci_planned2']) if request.form['ci_planned2'] else 1
        backboxinstallation_planned = int(request.form['backboxinstallation_planned']) if request.form['backboxinstallation_planned'] else 1
        baseinstallation_planned = int(request.form['baseinstallation_planned']) if request.form['baseinstallation_planned'] else 1
        detectorinstallation_planned = int(request.form['detectorinstallation_planned']) if request.form['detectorinstallation_planned'] else 1
        controlmoduleinstallation_planned = int(request.form['controlmoduleinstallation_planned']) if request.form['controlmoduleinstallation_planned'] else 1
        hooterinstallation_planned = int(request.form['hooterinstallation_planned']) if request.form['hooterinstallation_planned'] else 1
        mcpinstallation_planned = int(request.form['mcpinstallation_planned']) if request.form['mcpinstallation_planned'] else 1
        responseindicatorinstallation_planned = int(request.form['responseindicatorinstallation_planned']) if request.form['responseindicatorinstallation_planned'] else 1
        monitormoduleinstallation_planned = int(request.form['monitormoduleinstallation_planned']) if request.form['monitormoduleinstallation_planned'] else 1
        controlrelaymoduleinstallation_planned = int(request.form['controlrelaymoduleinstallation_planned']) if request.form['controlrelaymoduleinstallation_planned'] else 1
        isolatormoduleinstallation_planned = int(request.form['isolatormoduleinstallation_planned']) if request.form['isolatormoduleinstallation_planned'] else 1
        paspeakerinstallation_planned = int(request.form['paspeakerinstallation_planned']) if request.form['paspeakerinstallation_planned'] else 1
        twtbbackboxinstallation_planned = int(request.form['twtbbackboxinstallation_planned']) if request.form['twtbbackboxinstallation_planned'] else 1
        twtbspeakerinstallation_planned = int(request.form['twtbspeakerinstallation_planned']) if request.form['twtbspeakerinstallation_planned'] else 1
        firepanelinstallation_planned = int(request.form['firepanelinstallation_planned']) if request.form['firepanelinstallation_planned'] else 1
        pacontrollerinstallation_planned = int(request.form['pacontrollerinstallation_planned']) if request.form['pacontrollerinstallation_planned'] else 1
        twtbcontrollerinstallation_planned = int(request.form['twtbcontrollerinstallation_planned']) if request.form['twtbcontrollerinstallation_planned'] else 1
        smpsinstallation_planned = int(request.form['smpsinstallation_planned']) if request.form['smpsinstallation_planned'] else 1
        detectortesting_planned = int(request.form['detectortesting_planned']) if request.form['detectortesting_planned'] else 1
        continuitytesting_planned = int(request.form['continuitytesting_planned']) if request.form['continuitytesting_planned'] else 1
        programming_planned = int(request.form['programming_planned']) if request.form['programming_planned'] else 1
        continuitytesting_planned1 = int(request.form['continuitytesting_planned1']) if request.form['continuitytesting_planned1'] else 1
        programming_planned1 = int(request.form['programming_planned1']) if request.form['programming_planned1'] else 1
        continuitytesting_planned2 = int(request.form['continuitytesting_planned2']) if request.form['continuitytesting_planned2'] else 1
        programming_planned2 = int(request.form['programming_planned2']) if request.form['programming_planned2'] else 1
        
        chippingplasting_planned = int(request.form['chippingplasting_planned']) if request.form['chippingplasting_planned'] else 1
        handingoverdocument_planned = int(request.form['handingoverdocument_planned']) if request.form['handingoverdocument_planned'] else 1

        # Delete previous planned data for the current user
        Planned.query.filter_by(user_id=current_user.id).delete()
        Contact.query.filter_by(user_id=current_user.id).delete()

        # Add new contact details
        new_contact = Contact(
            name1=name1,
            name2=name2,
            email1=email1,
            email2=email2,
            contact1=contact1,
            contact2=contact2,
            user_id=current_user.id
        )
        db.session.add(new_contact)

        # Add new planned data
        new_data = Planned(
            start=start,
            cable_planned=cable_planned,
            pvc_planned=pvc_planned,
            mark_planned=mark_planned,
            ci_planned=ci_planned,
            pvc_planned1=pvc_planned1,
            mark_planned1=mark_planned1,
            ci_planned1=ci_planned1,
            cable_planned2=cable_planned2,
            pvc_planned2=pvc_planned2,
            mark_planned2=mark_planned2,
            ci_planned2=ci_planned2,
            backboxinstallation_planned=backboxinstallation_planned,
            baseinstallation_planned=baseinstallation_planned,
            detectorinstallation_planned=detectorinstallation_planned,
            controlmoduleinstallation_planned=controlmoduleinstallation_planned,
            hooterinstallation_planned=hooterinstallation_planned,
            mcpinstallation_planned=mcpinstallation_planned,
            responseindicatorinstallation_planned=responseindicatorinstallation_planned,
            monitormoduleinstallation_planned=monitormoduleinstallation_planned,
            controlrelaymoduleinstallation_planned=controlrelaymoduleinstallation_planned,
            isolatormoduleinstallation_planned=isolatormoduleinstallation_planned,
            paspeakerinstallation_planned=paspeakerinstallation_planned,
            twtbbackboxinstallation_planned=twtbbackboxinstallation_planned,
            twtbspeakerinstallation_planned=twtbspeakerinstallation_planned,
            firepanelinstallation_planned=firepanelinstallation_planned,
            pacontrollerinstallation_planned=pacontrollerinstallation_planned,
            twtbcontrollerinstallation_planned=twtbcontrollerinstallation_planned,
            smpsinstallation_planned=smpsinstallation_planned,
            detectortesting_planned=detectortesting_planned,
            continuitytesting_planned=continuitytesting_planned,
            programming_planned=programming_planned,
            continuitytesting_planned1=continuitytesting_planned1,
            programming_planned1=programming_planned1,
            continuitytesting_planned2=continuitytesting_planned2,
            programming_planned2=programming_planned2,
            chippingplasting_planned=chippingplasting_planned,
            handingoverdocument_planned=handingoverdocument_planned,
            user_id=current_user.id
        )
        db.session.add(new_data)

        # Iterate through form data lists and save to database
        for i in range(len(uniquees)):
            uniquee_value = uniquees[i] if uniquees[i] else None
            existing_manday = ManDay.query.filter_by(uniquee=uniquee_value, user_id=current_user.id).first()

            if existing_manday:
                # Update existing record
                existing_manday.day = int(days[i]) if days[i] else 0
                existing_manday.date = dates[i] if dates[i] else ''
                existing_manday.sdate = sdates[i] if sdates[i] else ''
                existing_manday.site = sites[i] if sites[i] else ''
                existing_manday.sub = subs[i] if subs[i] else ''
                existing_manday.remarks = remarks_list[i] if remarks_list[i] else ''
                existing_manday.support = supports[i] if supports[i] else ''
                existing_manday.support1 = support1s[i] if support1s[i] else ''
                existing_manday.cable = int(cables[i]) if cables[i] else 0
                existing_manday.pvc = int(pvcs[i]) if pvcs[i] else 0
                existing_manday.markingdrilling = int(markingDrillings[i]) if markingDrillings[i] else 0
                existing_manday.ci = int(cis[i]) if cis[i] else 0
                existing_manday.pvc1 = int(pvcs1[i]) if pvcs1[i] else 0
                existing_manday.markingdrilling1 = int(markingDrillings1[i]) if markingDrillings1[i] else 0
                existing_manday.ci1 = int(cis1[i]) if cis1[i] else 0
                
                existing_manday.pvc2 = int(pvcs2[i]) if pvcs2[i] else 0
                existing_manday.markingdrilling2 = int(markingDrillings2[i]) if markingDrillings2[i] else 0
                existing_manday.ci2 = int(cis2[i]) if cis2[i] else 0
                existing_manday.backboxinstallation = int(backboxInstallations[i]) if backboxInstallations[i] else 0
                existing_manday.baseinstallation = int(baseInstallations[i]) if baseInstallations[i] else 0
                existing_manday.detectorinstallation = int(detectorInstallations[i]) if detectorInstallations[i] else 0
                existing_manday.controlmoduleinstallation = int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0
                existing_manday.hooterinstallation = int(hooterInstallations[i]) if hooterInstallations[i] else 0
                existing_manday.mcpinstallation = int(mcpInstallations[i]) if mcpInstallations[i] else 0
                existing_manday.responseindicatorinstallation = int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0
                existing_manday.monitormoduleinstallation = int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0
                existing_manday.controlrelaymoduleinstallation = int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0
                existing_manday.isolatormoduleinstallation = int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0
                existing_manday.paspeakerinstallation = int(paSpeakerInstallations[i]) if paSpeakerInstallations[i] else 0
                existing_manday.twtbbackboxinstallation = int(twtbBackboxInstallations[i]) if twtbBackboxInstallations[i] else 0
                existing_manday.twtbspeakerinstallation = int(twtbSpeakerInstallations[i]) if twtbSpeakerInstallations[i] else 0
                existing_manday.firepanelinstallation = int(firePanelInstallations[i]) if firePanelInstallations[i] else 0
                existing_manday.pacontrollerinstallation = int(paControllerInstallations[i]) if paControllerInstallations[i] else 0
                existing_manday.twtbcontrollerinstallation = int(twtbControllerInstallations[i]) if twtbControllerInstallations[i] else 0
                existing_manday.smpsinstallation = int(smpsInstallations[i]) if smpsInstallations[i] else 0
                existing_manday.detectortesting = int(detectorTestings[i]) if detectorTestings[i] else 0
                existing_manday.continuitytesting = int(continuityTestings[i]) if continuityTestings[i] else 0
                existing_manday.programming = int(programmings[i]) if programmings[i] else 0
                existing_manday.continuitytesting1 = int(continuityTestings1[i]) if continuityTestings1[i] else 0
                existing_manday.programming1 = int(programmings1[i]) if programmings1[i] else 0
                existing_manday.continuitytesting2 = int(continuityTestings2[i]) if continuityTestings2[i] else 0
                existing_manday.programming2 = int(programmings2[i]) if programmings2[i] else 0
                existing_manday.chippingplasting = int(chippingPlastings[i]) if chippingPlastings[i] else 0
                existing_manday.handingoverdocument = int(handingOverDocuments[i]) if handingOverDocuments[i] else 0
            else:
                # Insert new record
                new_manday = ManDay(
                    uniquee=uniquee_value,
                    day=int(days[i]) if days[i] else 0,
                    date=dates[i] if dates[i] else '',
                    sdate=sdates[i] if sdates[i] else '',
                    site=sites[i] if sites[i] else '',
                    sub=subs[i] if subs[i] else '',
                    remarks=remarks_list[i] if remarks_list[i] else '',
                    support=supports[i] if supports[i] else '',
                    support1=support1s[i] if support1s[i] else '',
                    cable=int(cables[i]) if cables[i] else 0,
                    pvc=int(pvcs[i]) if pvcs[i] else 0,
                    markingdrilling=int(markingDrillings[i]) if markingDrillings[i] else 0,
                    ci=int(cis[i]) if cis[i] else 0,
                    pvc1=int(pvcs1[i]) if pvcs1[i] else 0,
                    markingdrilling1=int(markingDrillings1[i]) if markingDrillings1[i] else 0,
                    ci1=int(cis1[i]) if cis1[i] else 0,
                   
                    pvc2=int(pvcs2[i]) if pvcs2[i] else 0,
                    markingdrilling2=int(markingDrillings2[i]) if markingDrillings2[i] else 0,
                    ci2=int(cis2[i]) if cis2[i] else 0,
                    backboxinstallation=int(backboxInstallations[i]) if backboxInstallations[i] else 0,
                    baseinstallation=int(baseInstallations[i]) if baseInstallations[i] else 0,
                    detectorinstallation=int(detectorInstallations[i]) if detectorInstallations[i] else 0,
                    controlmoduleinstallation=int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0,
                    hooterinstallation=int(hooterInstallations[i]) if hooterInstallations[i] else 0,
                    mcpinstallation=int(mcpInstallations[i]) if mcpInstallations[i] else 0,
                    responseindicatorinstallation=int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0,
                    monitormoduleinstallation=int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0,
                    controlrelaymoduleinstallation=int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0,
                    isolatormoduleinstallation=int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0,
                    paspeakerinstallation=int(paSpeakerInstallations[i]) if paSpeakerInstallations[i] else 0,
                    twtbbackboxinstallation=int(twtbBackboxInstallations[i]) if twtbBackboxInstallations[i] else 0,
                    twtbspeakerinstallation=int(twtbSpeakerInstallations[i]) if twtbSpeakerInstallations[i] else 0,
                    firepanelinstallation=int(firePanelInstallations[i]) if firePanelInstallations[i] else 0,
                    pacontrollerinstallation=int(paControllerInstallations[i]) if paControllerInstallations[i] else 0,
                    twtbcontrollerinstallation=int(twtbControllerInstallations[i]) if twtbControllerInstallations[i] else 0,
                    smpsinstallation=int(smpsInstallations[i]) if smpsInstallations[i] else 0,
                    detectortesting=int(detectorTestings[i]) if detectorTestings[i] else 0,
                    continuitytesting=int(continuityTestings[i]) if continuityTestings[i] else 0,
                    programming=int(programmings[i]) if programmings[i] else 0,
                    continuitytesting1=int(continuityTestings1[i]) if continuityTestings1[i] else 0,
                    programming1=int(programmings1[i]) if programmings1[i] else 0,
                    continuitytesting2=int(continuityTestings2[i]) if continuityTestings2[i] else 0,
                    programming2=int(programmings2[i]) if programmings2[i] else 0,
                    chippingplasting=int(chippingPlastings[i]) if chippingPlastings[i] else 0,
                    handingoverdocument=int(handingOverDocuments[i]) if handingOverDocuments[i] else 0,
                    user_id=current_user.id
                )
                db.session.add(new_manday)

        # Commit all changes
        db.session.commit()

        # Redirect to output page after successful submission
        return redirect(url_for('views.output'))

    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving the data.'}), 500


@views.route('/delete/<email>', methods=['DELETE'])
def delete_email(email):
    user = User.query.filter_by(email=email).first()

    if user:
        # Delete related records in other tables
        try:
            Product.query.filter_by(user_id=user.id).delete()
            Info.query.filter_by(user_id=user.id).delete()
            ManDay.query.filter_by(user_id=user.id).delete()
            Planned.query.filter_by(user_id=user.id).delete()
            Contact.query.filter_by(user_id=user.id).delete()

            # Delete the user itself
            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': f'User {email} and related records deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': f'User with email {email} not found'}), 404


@views.route('/stock')
@login_required
def stock():
    products = Stock.query.filter_by(user_id=current_user.id).all()
    email = current_user.email

    return render_template('stock.html', products=products,email = email)


@views.route('/add_stock', methods=['POST'])
@login_required
def add_stock():
    menus = request.form.getlist('menu[]')
    items = request.form.getlist('item[]')
    makes = request.form.getlist('make[]')
    units = [int(u) if u else 0 for u in request.form.getlist('unit[]')]
    iofs = request.form.getlist('iof[]')
    stocks = request.form.getlist('stock[]')
    cumulatives = units + stocks
    dates1 = request.form.getlist('date1[]')
    remarks1s = request.form.getlist('remarks1[]')
    dates2 = request.form.getlist('date2[]')
    remarks2s = request.form.getlist('remarks2[]')

    units_raw = request.form.getlist('unit[]')
    print("Raw units data:", units_raw)

    for i in range(len(items)):
        item = items[i]
        existing_product = Stock.query.filter_by(item=item, user_id=current_user.id).first()

        if existing_product:
            # Update existing product
            existing_product.menu = menus[i]
            existing_product.make = makes[i]
            existing_product.iof = int(iofs[i]) if iofs[i] else 0
            existing_product.stock = int(stocks[i]) if stocks[i] else 0
            existing_product.unit = int(units[i]) if units[i] else 0
            existing_product.cumulative = int(units[i]) + int(stocks[i]) if(int(units[i]) + int(stocks[i])) else 0
            existing_product.date1 = dates1[i]
            existing_product.remarks1 = remarks1s[i]
            existing_product.date2 = dates2[i]
            existing_product.remarks2 = remarks2s[i]
        else:
            # Create new product
            new = Stock(
                item=item,
                menu=menus[i],
                make=makes[i],

                iof=int(iofs[i]) if iofs[i] else 0,
                stock=int(stocks[i]) if stocks[i] else 0,
                 unit=int(units[i]) if units[i] else 0,
                cumulative = int(units[i]) + int(stocks[i]) if(int(units[i]) + int(stocks[i])) else 0 ,
                date1=dates1[i],
                remarks1=remarks1s[i],
                date2=dates2[i],
                remarks2=remarks2s[i],
                user_id=current_user.id
            )
            db.session.add(new)
            db.session.commit()

    try:
        db.session.commit()
        return redirect(url_for('views.display1'))
    except Exception as e:
        db.session.rollback()
        print(f"Error committing to database: {str(e)}")
        # Handle error appropriately, e.g., render an error page
        return render_template('error.html', error=str(e))



@views.route('/display1')
@login_required
def display1():
    stonks = Stock.query.filter_by(user_id=current_user.id).all()
    infos = db.session.query(Info).filter(Info.user_id == current_user.id).all()
    contact = db.session.query(Contact).filter(Contact.user_id == current_user.id).all()
    current_date = datetime.now().strftime('%d-%m-%Y')

    return render_template('display1.html', stonks=stonks, infos = infos , contact=contact, current_date = current_date)

@views.route('/delete_product2/<int:id>', methods=['DELETE'])
def delete_product2(id):
    try:
        product = Stock.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of exception
        return jsonify({'status': 'error', 'message': str(e)}), 500
    



@views.route('/save_datafas1', methods=['POST'])
@login_required
def save_datafas1():
    try:
        # Extract form data from POST request
        uniquees = request.form.getlist('uniquee[]')
        days = request.form.getlist('day[]')
        dates = request.form.getlist('date[]')
        sdates = request.form.getlist('sdate[]')
        sites = request.form.getlist('site[]')
        subs = request.form.getlist('sub[]')
        remarks_list = request.form.getlist('remarks[]')
        supports = request.form.getlist('support[]')
        support1s = request.form.getlist('support1[]')
        cables = request.form.getlist('cable[]')
        pvcs = request.form.getlist('pvc[]')
        markingDrillings = request.form.getlist('markingdrilling[]')
        cis = request.form.getlist('ci[]')
        backboxInstallations = request.form.getlist('backboxinstallation[]')
        baseInstallations = request.form.getlist('baseinstallation[]')
        detectorInstallations = request.form.getlist('detectorinstallation[]')
        controlModuleInstallations = request.form.getlist('controlmoduleinstallation[]')
        hooterInstallations = request.form.getlist('hooterinstallation[]')
        mcpInstallations = request.form.getlist('mcpinstallation[]')
        responseIndicatorInstallations = request.form.getlist('responseindicatorinstallation[]')
        monitorModuleInstallations = request.form.getlist('monitormoduleinstallation[]')
        controlRelayModuleInstallations = request.form.getlist('controlrelaymoduleinstallation[]')
        isolatorModuleInstallations = request.form.getlist('isolatormoduleinstallation[]')
        firePanelInstallations = request.form.getlist('firepanelinstallation[]')
        smpsInstallations = request.form.getlist('smpsinstallation[]')
        detectorTestings = request.form.getlist('detectortesting[]')
        continuityTestings = request.form.getlist('continuitytesting[]')
        programmings = request.form.getlist('programming[]')
        chippingPlastings = request.form.getlist('chippingplasting[]')
        handingOverDocuments = request.form.getlist('handingoverdocument[]')

        # Contact details
        name1 = request.form['name1'] if request.form['name1'] else ''
        name2 = request.form['name2'] if request.form['name2'] else ''
        email1 = request.form['email1'] if request.form['email1'] else ''
        email2 = request.form['email2'] if request.form['email2'] else ''
        contact1 = int(request.form['contact1']) if request.form['contact1'] else 0
        contact2 = int(request.form['contact2']) if request.form['contact2'] else 0

        # Planned data
        start = request.form['start'] if request.form['start'] else ''
        cable_planned = int(request.form['cable_planned']) if request.form['cable_planned'] else 1
        pvc_planned = int(request.form['pvc_planned']) if request.form['pvc_planned'] else 1
        mark_planned = int(request.form['mark_planned']) if request.form['mark_planned'] else 1
        ci_planned = int(request.form['ci_planned']) if request.form['ci_planned'] else 1
        backboxinstallation_planned = int(request.form['backboxinstallation_planned']) if request.form['backboxinstallation_planned'] else 1
        baseinstallation_planned = int(request.form['baseinstallation_planned']) if request.form['baseinstallation_planned'] else 1
        detectorinstallation_planned = int(request.form['detectorinstallation_planned']) if request.form['detectorinstallation_planned'] else 1
        controlmoduleinstallation_planned = int(request.form['controlmoduleinstallation_planned']) if request.form['controlmoduleinstallation_planned'] else 1
        hooterinstallation_planned = int(request.form['hooterinstallation_planned']) if request.form['hooterinstallation_planned'] else 1
        mcpinstallation_planned = int(request.form['mcpinstallation_planned']) if request.form['mcpinstallation_planned'] else 1
        responseindicatorinstallation_planned = int(request.form['responseindicatorinstallation_planned']) if request.form['responseindicatorinstallation_planned'] else 1
        monitormoduleinstallation_planned = int(request.form['monitormoduleinstallation_planned']) if request.form['monitormoduleinstallation_planned'] else 1
        controlrelaymoduleinstallation_planned = int(request.form['controlrelaymoduleinstallation_planned']) if request.form['controlrelaymoduleinstallation_planned'] else 1
        isolatormoduleinstallation_planned = int(request.form['isolatormoduleinstallation_planned']) if request.form['isolatormoduleinstallation_planned'] else 1
        firepanelinstallation_planned = int(request.form['firepanelinstallation_planned']) if request.form['firepanelinstallation_planned'] else 1
        smpsinstallation_planned = int(request.form['smpsinstallation_planned']) if request.form['smpsinstallation_planned'] else 1
        detectortesting_planned = int(request.form['detectortesting_planned']) if request.form['detectortesting_planned'] else 1
        continuitytesting_planned = int(request.form['continuitytesting_planned']) if request.form['continuitytesting_planned'] else 1
        programming_planned = int(request.form['programming_planned']) if request.form['programming_planned'] else 1
        chippingplasting_planned = int(request.form['chippingplasting_planned']) if request.form['chippingplasting_planned'] else 1
        handingoverdocument_planned = int(request.form['handingoverdocument_planned']) if request.form['handingoverdocument_planned'] else 1

        # Delete previous planned data for the current user
        Planned.query.filter_by(user_id=current_user.id).delete()
        Contact.query.filter_by(user_id=current_user.id).delete()

        # Add new contact details
        new_contact = Contact(
            name1=name1,
            name2=name2,
            email1=email1,
            email2=email2,
            contact1=contact1,
            contact2=contact2,
            user_id=current_user.id
        )
        db.session.add(new_contact)

        # Add new planned data
        new_data = Planned(
            start=start,
            cable_planned=cable_planned,
            pvc_planned=pvc_planned,
            mark_planned=mark_planned,
            ci_planned=ci_planned,
            backboxinstallation_planned=backboxinstallation_planned,
            baseinstallation_planned=baseinstallation_planned,
            detectorinstallation_planned=detectorinstallation_planned,
            controlmoduleinstallation_planned=controlmoduleinstallation_planned,
            hooterinstallation_planned=hooterinstallation_planned,
            mcpinstallation_planned=mcpinstallation_planned,
            responseindicatorinstallation_planned=responseindicatorinstallation_planned,
            monitormoduleinstallation_planned=monitormoduleinstallation_planned,
            controlrelaymoduleinstallation_planned=controlrelaymoduleinstallation_planned,
            isolatormoduleinstallation_planned=isolatormoduleinstallation_planned,
         
            firepanelinstallation_planned=firepanelinstallation_planned,
           
            smpsinstallation_planned=smpsinstallation_planned,
            detectortesting_planned=detectortesting_planned,
            continuitytesting_planned=continuitytesting_planned,
            programming_planned=programming_planned,
            chippingplasting_planned=chippingplasting_planned,
            handingoverdocument_planned=handingoverdocument_planned,
            user_id=current_user.id
        )
        db.session.add(new_data)

        # Iterate through form data lists and save to database
        for i in range(len(uniquees)):
            uniquee_value = uniquees[i] if uniquees[i] else None
            existing_manday = ManDay.query.filter_by(uniquee=uniquee_value, user_id=current_user.id).first()

            if existing_manday:
                # Update existing record
                existing_manday.day = int(days[i]) if days[i] else 0
                existing_manday.date = dates[i] if dates[i] else ''
                existing_manday.sdate = sdates[i] if sdates[i] else ''
                existing_manday.site = sites[i] if sites[i] else ''
                existing_manday.sub = subs[i] if subs[i] else ''
                existing_manday.remarks = remarks_list[i] if remarks_list[i] else ''
                existing_manday.support = supports[i] if supports[i] else ''
                existing_manday.support1 = support1s[i] if support1s[i] else ''
                existing_manday.cable = int(cables[i]) if cables[i] else 0
                existing_manday.pvc = int(pvcs[i]) if pvcs[i] else 0
                existing_manday.markingdrilling = int(markingDrillings[i]) if markingDrillings[i] else 0
                existing_manday.ci = int(cis[i]) if cis[i] else 0
                existing_manday.backboxinstallation = int(backboxInstallations[i]) if backboxInstallations[i] else 0
                existing_manday.baseinstallation = int(baseInstallations[i]) if baseInstallations[i] else 0
                existing_manday.detectorinstallation = int(detectorInstallations[i]) if detectorInstallations[i] else 0
                existing_manday.controlmoduleinstallation = int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0
                existing_manday.hooterinstallation = int(hooterInstallations[i]) if hooterInstallations[i] else 0
                existing_manday.mcpinstallation = int(mcpInstallations[i]) if mcpInstallations[i] else 0
                existing_manday.responseindicatorinstallation = int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0
                existing_manday.monitormoduleinstallation = int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0
                existing_manday.controlrelaymoduleinstallation = int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0
                existing_manday.isolatormoduleinstallation = int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0
                existing_manday.firepanelinstallation = int(firePanelInstallations[i]) if firePanelInstallations[i] else 0
                existing_manday.smpsinstallation = int(smpsInstallations[i]) if smpsInstallations[i] else 0
                existing_manday.detectortesting = int(detectorTestings[i]) if detectorTestings[i] else 0
                existing_manday.continuitytesting = int(continuityTestings[i]) if continuityTestings[i] else 0
                existing_manday.programming = int(programmings[i]) if programmings[i] else 0
                existing_manday.chippingplasting = int(chippingPlastings[i]) if chippingPlastings[i] else 0
                existing_manday.handingoverdocument = int(handingOverDocuments[i]) if handingOverDocuments[i] else 0
            else:
                # Insert new record
                new_manday = ManDay(
                    uniquee=uniquee_value,
                    day=int(days[i]) if days[i] else 0,
                    date=dates[i] if dates[i] else '',
                    sdate=sdates[i] if sdates[i] else '',
                    site=sites[i] if sites[i] else '',
                    sub=subs[i] if subs[i] else '',
                    remarks=remarks_list[i] if remarks_list[i] else '',
                    support=supports[i] if supports[i] else '',
                    support1=support1s[i] if support1s[i] else '',
                    cable=int(cables[i]) if cables[i] else 0,
                    pvc=int(pvcs[i]) if pvcs[i] else 0,
                    markingdrilling=int(markingDrillings[i]) if markingDrillings[i] else 0,
                    ci=int(cis[i]) if cis[i] else 0,
                    backboxinstallation=int(backboxInstallations[i]) if backboxInstallations[i] else 0,
                    baseinstallation=int(baseInstallations[i]) if baseInstallations[i] else 0,
                    detectorinstallation=int(detectorInstallations[i]) if detectorInstallations[i] else 0,
                    controlmoduleinstallation=int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0,
                    hooterinstallation=int(hooterInstallations[i]) if hooterInstallations[i] else 0,
                    mcpinstallation=int(mcpInstallations[i]) if mcpInstallations[i] else 0,
                    responseindicatorinstallation=int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0,
                    monitormoduleinstallation=int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0,
                    controlrelaymoduleinstallation=int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0,
                    isolatormoduleinstallation=int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0,
                    firepanelinstallation=int(firePanelInstallations[i]) if firePanelInstallations[i] else 0,
                    smpsinstallation=int(smpsInstallations[i]) if smpsInstallations[i] else 0,
                    detectortesting=int(detectorTestings[i]) if detectorTestings[i] else 0,
                    continuitytesting=int(continuityTestings[i]) if continuityTestings[i] else 0,
                    programming=int(programmings[i]) if programmings[i] else 0,
                    chippingplasting=int(chippingPlastings[i]) if chippingPlastings[i] else 0,
                    handingoverdocument=int(handingOverDocuments[i]) if handingOverDocuments[i] else 0,
                    user_id=current_user.id
                )
                db.session.add(new_manday)

        # Commit all changes
        db.session.commit()

        # Redirect to output page after successful submission
        return redirect(url_for('views.outputfas1'))

    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving the data.'}), 500


@views.route('/outputfas1')
@login_required
def outputfas1():
    mandays = (
        db.session.query(ManDay)
        .filter(ManDay.user_id == current_user.id)
        .group_by(ManDay.uniquee)
        .all()
    )
    rec = ManDay.query.filter(ManDay.user_id == current_user.id, ManDay.remarks.isnot('')).all()

    planned = db.session.query(Planned).filter(Planned.user_id == current_user.id).first()
    contact = db.session.query(Contact).filter(Contact.user_id == current_user.id).first()
    products = Product.query.filter_by(user_id=current_user.id).all()
    infos = db.session.query(Info).filter(Info.user_id == current_user.id).all()
    current_date = datetime.now().strftime('%d-%m-%Y')


    # Sum the actual values from the mandays records
    cable_actual = sum(manday.cable for manday in mandays if manday.cable)
    pvc_actual = sum(manday.pvc for manday in mandays if manday.pvc)
    mark_actual = sum(manday.markingdrilling for manday in mandays if manday.markingdrilling)
    ci_actual = sum(manday.ci for manday in mandays if manday.ci)
    backboxinstallation_actual = sum(manday.backboxinstallation for manday in mandays if manday.backboxinstallation)
    baseinstallation_actual = sum(manday.baseinstallation for manday in mandays if manday.baseinstallation)
    detectorinstallation_actual = sum(manday.detectorinstallation for manday in mandays if manday.detectorinstallation)
    controlmoduleinstallation_actual = sum(manday.controlmoduleinstallation for manday in mandays if manday.controlmoduleinstallation)
    hooterinstallation_actual = sum(manday.hooterinstallation for manday in mandays if manday.hooterinstallation)
    mcpinstallation_actual = sum(manday.mcpinstallation for manday in mandays if manday.mcpinstallation)
    responseindicatorinstallation_actual = sum(manday.responseindicatorinstallation for manday in mandays if manday.responseindicatorinstallation)
    monitormoduleinstallation_actual = sum(manday.monitormoduleinstallation for manday in mandays if manday.monitormoduleinstallation)
    controlrelaymoduleinstallation_actual = sum(manday.controlrelaymoduleinstallation for manday in mandays if manday.controlrelaymoduleinstallation)
    isolatormoduleinstallation_actual = sum(manday.isolatormoduleinstallation for manday in mandays if manday.isolatormoduleinstallation)
    firepanelinstallation_actual = sum(manday.firepanelinstallation for manday in mandays if manday.firepanelinstallation)
    smpsinstallation_actual = sum(manday.smpsinstallation for manday in mandays if manday.smpsinstallation)
    detectortesting_actual = sum(manday.detectortesting for manday in mandays if manday.detectortesting)
    continuitytesting_actual = sum(manday.continuitytesting for manday in mandays if manday.continuitytesting)
    programming_actual = sum(manday.programming for manday in mandays if manday.programming)
    chippingplasting_actual = sum(manday.chippingplasting for manday in mandays if manday.chippingplasting)
    handingoverdocument_actual = sum(manday.handingoverdocument for manday in mandays if manday.handingoverdocument)
    
    user_type = current_user.p_type
    if user_type == 'FAS1':
        return render_template(
        'outputfas1.html', products = products, infos = infos,current_date = current_date,
        records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
    )
    elif user_type == 'FAS2':
        return render_template(
        'outputfas2.html', products = products, infos = infos,current_date = current_date,
        records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
    )

@views.route('/outputfas3')
@login_required
def outputfas3():
    mandays = (
        db.session.query(ManDay)
        .filter(ManDay.user_id == current_user.id)
        .group_by(ManDay.uniquee)
        .all()
    )
    rec = ManDay.query.filter(ManDay.user_id == current_user.id, ManDay.remarks.isnot('')).all()

    planned = db.session.query(Planned).filter(Planned.user_id == current_user.id).first()
    contact = db.session.query(Contact).filter(Contact.user_id == current_user.id).first()
    products = Product.query.filter_by(user_id=current_user.id).all()
    infos = db.session.query(Info).filter(Info.user_id == current_user.id).all()
    current_date = datetime.now().strftime('%d-%m-%Y')


    # Sum the actual values from the mandays records
    cable_actual = sum(manday.cable for manday in mandays if manday.cable)
    pvc_actual = sum(manday.pvc for manday in mandays if manday.pvc)
    mark_actual = sum(manday.markingdrilling for manday in mandays if manday.markingdrilling)
    ci_actual = sum(manday.ci for manday in mandays if manday.ci)

    
    
    pvc_actual1 = sum(manday.pvc1 for manday in mandays if manday.pvc1)
    mark_actual1 = sum(manday.markingdrilling1 for manday in mandays if manday.markingdrilling1)
    ci_actual1 = sum(manday.ci1 for manday in mandays if manday.ci1)

    backboxinstallation_actual = sum(manday.backboxinstallation for manday in mandays if manday.backboxinstallation)
    baseinstallation_actual = sum(manday.baseinstallation for manday in mandays if manday.baseinstallation)
    detectorinstallation_actual = sum(manday.detectorinstallation for manday in mandays if manday.detectorinstallation)
    controlmoduleinstallation_actual = sum(manday.controlmoduleinstallation for manday in mandays if manday.controlmoduleinstallation)
    hooterinstallation_actual = sum(manday.hooterinstallation for manday in mandays if manday.hooterinstallation)
    mcpinstallation_actual = sum(manday.mcpinstallation for manday in mandays if manday.mcpinstallation)
    responseindicatorinstallation_actual = sum(manday.responseindicatorinstallation for manday in mandays if manday.responseindicatorinstallation)
    monitormoduleinstallation_actual = sum(manday.monitormoduleinstallation for manday in mandays if manday.monitormoduleinstallation)
    controlrelaymoduleinstallation_actual = sum(manday.controlrelaymoduleinstallation for manday in mandays if manday.controlrelaymoduleinstallation)
    isolatormoduleinstallation_actual = sum(manday.isolatormoduleinstallation for manday in mandays if manday.isolatormoduleinstallation)
    paspeakerinstallation_actual = sum(manday.paspeakerinstallation for manday in mandays if manday.paspeakerinstallation)
    firepanelinstallation_actual = sum(manday.firepanelinstallation for manday in mandays if manday.firepanelinstallation)
    pacontrollerinstallation_actual = sum(manday.pacontrollerinstallation for manday in mandays if manday.pacontrollerinstallation)
    smpsinstallation_actual = sum(manday.smpsinstallation for manday in mandays if manday.smpsinstallation)
    detectortesting_actual = sum(manday.detectortesting for manday in mandays if manday.detectortesting)
    continuitytesting_actual = sum(manday.continuitytesting for manday in mandays if manday.continuitytesting)
    programming_actual = sum(manday.programming for manday in mandays if manday.programming)

    continuitytesting_actual1 = sum(manday.continuitytesting1 for manday in mandays if manday.continuitytesting1)
    programming_actual1 = sum(manday.programming1 for manday in mandays if manday.programming1)

    chippingplasting_actual = sum(manday.chippingplasting for manday in mandays if manday.chippingplasting)
    handingoverdocument_actual = sum(manday.handingoverdocument for manday in mandays if manday.handingoverdocument)

    user_type = current_user.p_type
    if user_type == 'FAS+PA1':
        return render_template(
        'outputfas3.html', products = products, infos = infos,current_date = current_date,
        records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        pvc_actual1=pvc_actual1,
        mark_actual1=mark_actual1,
        ci_actual1=ci_actual1,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        paspeakerinstallation_actual=paspeakerinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        pacontrollerinstallation_actual=pacontrollerinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        continuitytesting_actual1=continuitytesting_actual1,
        programming_actual1=programming_actual1,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
     )
    
    elif user_type == 'FAS+PA2':
        return render_template(
        'outputfas4.html', products = products, infos = infos,current_date = current_date,
 records=mandays,
        planned=planned, contact = contact,
        cable_actual=cable_actual,
        pvc_actual=pvc_actual,
        mark_actual=mark_actual,
        ci_actual=ci_actual,
        pvc_actual1=pvc_actual1,
        mark_actual1=mark_actual1,
        ci_actual1=ci_actual1,
        backboxinstallation_actual=backboxinstallation_actual,
        baseinstallation_actual=baseinstallation_actual,
        detectorinstallation_actual=detectorinstallation_actual,
        controlmoduleinstallation_actual=controlmoduleinstallation_actual,
        hooterinstallation_actual=hooterinstallation_actual,
        mcpinstallation_actual=mcpinstallation_actual,
        responseindicatorinstallation_actual=responseindicatorinstallation_actual,
        monitormoduleinstallation_actual=monitormoduleinstallation_actual,
        controlrelaymoduleinstallation_actual=controlrelaymoduleinstallation_actual,
        isolatormoduleinstallation_actual=isolatormoduleinstallation_actual,
        paspeakerinstallation_actual=paspeakerinstallation_actual,
        firepanelinstallation_actual=firepanelinstallation_actual,
        pacontrollerinstallation_actual=pacontrollerinstallation_actual,
        smpsinstallation_actual=smpsinstallation_actual,
        detectortesting_actual=detectortesting_actual,
        continuitytesting_actual=continuitytesting_actual,
        programming_actual=programming_actual,
        continuitytesting_actual1=continuitytesting_actual1,
        programming_actual1=programming_actual1,
        chippingplasting_actual=chippingplasting_actual,
        handingoverdocument_actual=handingoverdocument_actual,rec = rec
     )




@views.route('/save_datafas3', methods=['POST'])
@login_required
def save_datafas3():
    try:
        # Extract form data from POST request
        uniquees = request.form.getlist('uniquee[]')
        days = request.form.getlist('day[]')
        dates = request.form.getlist('date[]')
        sdates = request.form.getlist('sdate[]')
        sites = request.form.getlist('site[]')
        subs = request.form.getlist('sub[]')
        remarks_list = request.form.getlist('remarks[]')
        supports = request.form.getlist('support[]')
        support1s = request.form.getlist('support1[]')
        cables = request.form.getlist('cable[]')
        pvcs = request.form.getlist('pvc[]')
        markingDrillings = request.form.getlist('markingdrilling[]')
        cis = request.form.getlist('ci[]')
        pvcs1= request.form.getlist('pvc1[]')
        markingDrillings1 = request.form.getlist('markingdrilling1[]')
        cis1 = request.form.getlist('ci1[]')
        backboxInstallations = request.form.getlist('backboxinstallation[]')
        baseInstallations = request.form.getlist('baseinstallation[]')
        detectorInstallations = request.form.getlist('detectorinstallation[]')
        controlModuleInstallations = request.form.getlist('controlmoduleinstallation[]')
        hooterInstallations = request.form.getlist('hooterinstallation[]')
        mcpInstallations = request.form.getlist('mcpinstallation[]')
        responseIndicatorInstallations = request.form.getlist('responseindicatorinstallation[]')
        monitorModuleInstallations = request.form.getlist('monitormoduleinstallation[]')
        controlRelayModuleInstallations = request.form.getlist('controlrelaymoduleinstallation[]')
        isolatorModuleInstallations = request.form.getlist('isolatormoduleinstallation[]')
        paSpeakerInstallations = request.form.getlist('paspeakerinstallation[]')
        firePanelInstallations = request.form.getlist('firepanelinstallation[]')
        paControllerInstallations = request.form.getlist('pacontrollerinstallation[]')
        smpsInstallations = request.form.getlist('smpsinstallation[]')
        detectorTestings = request.form.getlist('detectortesting[]')
        continuityTestings = request.form.getlist('continuitytesting[]')
        programmings = request.form.getlist('programming[]')
        continuityTestings1 = request.form.getlist('continuitytesting1[]')
        programmings1 = request.form.getlist('programming1[]')
        chippingPlastings = request.form.getlist('chippingplasting[]')
        handingOverDocuments = request.form.getlist('handingoverdocument[]')

        # Contact details
        name1 = request.form['name1'] if request.form['name1'] else ''
        name2 = request.form['name2'] if request.form['name2'] else ''
        email1 = request.form['email1'] if request.form['email1'] else ''
        email2 = request.form['email2'] if request.form['email2'] else ''
        contact1 = int(request.form['contact1']) if request.form['contact1'] else 0
        contact2 = int(request.form['contact2']) if request.form['contact2'] else 0

        # Planned data
        start = request.form['start'] if request.form['start'] else ''
        cable_planned = int(request.form['cable_planned']) if request.form['cable_planned'] else 1
        pvc_planned = int(request.form['pvc_planned']) if request.form['pvc_planned'] else 1
        mark_planned = int(request.form['mark_planned']) if request.form['mark_planned'] else 1
        ci_planned = int(request.form['ci_planned']) if request.form['ci_planned'] else 1
        pvc_planned1 = int(request.form['pvc_planned1']) if request.form['pvc_planned1'] else 1
        mark_planned1 = int(request.form['mark_planned1']) if request.form['mark_planned1'] else 1
        ci_planned1 = int(request.form['ci_planned1']) if request.form['ci_planned1'] else 1
        backboxinstallation_planned = int(request.form['backboxinstallation_planned']) if request.form['backboxinstallation_planned'] else 1
        baseinstallation_planned = int(request.form['baseinstallation_planned']) if request.form['baseinstallation_planned'] else 1
        detectorinstallation_planned = int(request.form['detectorinstallation_planned']) if request.form['detectorinstallation_planned'] else 1
        controlmoduleinstallation_planned = int(request.form['controlmoduleinstallation_planned']) if request.form['controlmoduleinstallation_planned'] else 1
        hooterinstallation_planned = int(request.form['hooterinstallation_planned']) if request.form['hooterinstallation_planned'] else 1
        mcpinstallation_planned = int(request.form['mcpinstallation_planned']) if request.form['mcpinstallation_planned'] else 1
        responseindicatorinstallation_planned = int(request.form['responseindicatorinstallation_planned']) if request.form['responseindicatorinstallation_planned'] else 1
        monitormoduleinstallation_planned = int(request.form['monitormoduleinstallation_planned']) if request.form['monitormoduleinstallation_planned'] else 1
        controlrelaymoduleinstallation_planned = int(request.form['controlrelaymoduleinstallation_planned']) if request.form['controlrelaymoduleinstallation_planned'] else 1
        isolatormoduleinstallation_planned = int(request.form['isolatormoduleinstallation_planned']) if request.form['isolatormoduleinstallation_planned'] else 1
        paspeakerinstallation_planned = int(request.form['paspeakerinstallation_planned']) if request.form['paspeakerinstallation_planned'] else 1
        firepanelinstallation_planned = int(request.form['firepanelinstallation_planned']) if request.form['firepanelinstallation_planned'] else 1
        pacontrollerinstallation_planned = int(request.form['pacontrollerinstallation_planned']) if request.form['pacontrollerinstallation_planned'] else 1
        smpsinstallation_planned = int(request.form['smpsinstallation_planned']) if request.form['smpsinstallation_planned'] else 1
        detectortesting_planned = int(request.form['detectortesting_planned']) if request.form['detectortesting_planned'] else 1
        continuitytesting_planned = int(request.form['continuitytesting_planned']) if request.form['continuitytesting_planned'] else 1
        programming_planned = int(request.form['programming_planned']) if request.form['programming_planned'] else 1
        continuitytesting_planned1 = int(request.form['continuitytesting_planned1']) if request.form['continuitytesting_planned1'] else 1
        programming_planned1 = int(request.form['programming_planned1']) if request.form['programming_planned1'] else 1
        chippingplasting_planned = int(request.form['chippingplasting_planned']) if request.form['chippingplasting_planned'] else 1
        handingoverdocument_planned = int(request.form['handingoverdocument_planned']) if request.form['handingoverdocument_planned'] else 1

        # Delete previous planned data for the current user
        Planned.query.filter_by(user_id=current_user.id).delete()
        Contact.query.filter_by(user_id=current_user.id).delete()

        # Add new contact details
        new_contact = Contact(
            name1=name1,
            name2=name2,
            email1=email1,
            email2=email2,
            contact1=contact1,
            contact2=contact2,
            user_id=current_user.id
        )
        db.session.add(new_contact)

        # Add new planned data
        new_data = Planned(
            start=start,
            cable_planned=cable_planned,
            pvc_planned=pvc_planned,
            mark_planned=mark_planned,
            ci_planned=ci_planned,
            pvc_planned1=pvc_planned1,
            mark_planned1=mark_planned1,
            ci_planned1=ci_planned1,
            backboxinstallation_planned=backboxinstallation_planned,
            baseinstallation_planned=baseinstallation_planned,
            detectorinstallation_planned=detectorinstallation_planned,
            controlmoduleinstallation_planned=controlmoduleinstallation_planned,
            hooterinstallation_planned=hooterinstallation_planned,
            mcpinstallation_planned=mcpinstallation_planned,
            responseindicatorinstallation_planned=responseindicatorinstallation_planned,
            monitormoduleinstallation_planned=monitormoduleinstallation_planned,
            controlrelaymoduleinstallation_planned=controlrelaymoduleinstallation_planned,
            isolatormoduleinstallation_planned=isolatormoduleinstallation_planned,
            paspeakerinstallation_planned=paspeakerinstallation_planned,
            firepanelinstallation_planned=firepanelinstallation_planned,
            pacontrollerinstallation_planned=pacontrollerinstallation_planned,
            smpsinstallation_planned=smpsinstallation_planned,
            detectortesting_planned=detectortesting_planned,
            continuitytesting_planned=continuitytesting_planned,
            programming_planned=programming_planned,
            continuitytesting_planned1=continuitytesting_planned1,
            programming_planned1=programming_planned1,
            chippingplasting_planned=chippingplasting_planned,
            handingoverdocument_planned=handingoverdocument_planned,
            user_id=current_user.id
        )
        db.session.add(new_data)

        # Iterate through form data lists and save to database
        for i in range(len(uniquees)):
            uniquee_value = uniquees[i] if uniquees[i] else None
            existing_manday = ManDay.query.filter_by(uniquee=uniquee_value, user_id=current_user.id).first()

            if existing_manday:
                # Update existing record
                existing_manday.day = int(days[i]) if days[i] else 0
                existing_manday.date = dates[i] if dates[i] else ''
                existing_manday.sdate = sdates[i] if sdates[i] else ''
                existing_manday.site = sites[i] if sites[i] else ''
                existing_manday.sub = subs[i] if subs[i] else ''
                existing_manday.remarks = remarks_list[i] if remarks_list[i] else ''
                existing_manday.support = supports[i] if supports[i] else ''
                existing_manday.support1 = support1s[i] if support1s[i] else ''
                existing_manday.cable = int(cables[i]) if cables[i] else 0
                existing_manday.pvc = int(pvcs[i]) if pvcs[i] else 0
                existing_manday.markingdrilling = int(markingDrillings[i]) if markingDrillings[i] else 0
                existing_manday.ci = int(cis[i]) if cis[i] else 0
                existing_manday.pvc1 = int(pvcs1[i]) if pvcs1[i] else 0
                existing_manday.markingdrilling1 = int(markingDrillings1[i]) if markingDrillings1[i] else 0
                existing_manday.ci1 = int(cis1[i]) if cis1[i] else 0
                existing_manday.backboxinstallation = int(backboxInstallations[i]) if backboxInstallations[i] else 0
                existing_manday.baseinstallation = int(baseInstallations[i]) if baseInstallations[i] else 0
                existing_manday.detectorinstallation = int(detectorInstallations[i]) if detectorInstallations[i] else 0
                existing_manday.controlmoduleinstallation = int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0
                existing_manday.hooterinstallation = int(hooterInstallations[i]) if hooterInstallations[i] else 0
                existing_manday.mcpinstallation = int(mcpInstallations[i]) if mcpInstallations[i] else 0
                existing_manday.responseindicatorinstallation = int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0
                existing_manday.monitormoduleinstallation = int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0
                existing_manday.controlrelaymoduleinstallation = int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0
                existing_manday.isolatormoduleinstallation = int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0
                existing_manday.paspeakerinstallation = int(paSpeakerInstallations[i]) if paSpeakerInstallations[i] else 0
                existing_manday.firepanelinstallation = int(firePanelInstallations[i]) if firePanelInstallations[i] else 0
                existing_manday.pacontrollerinstallation = int(paControllerInstallations[i]) if paControllerInstallations[i] else 0
                existing_manday.smpsinstallation = int(smpsInstallations[i]) if smpsInstallations[i] else 0
                existing_manday.detectortesting = int(detectorTestings[i]) if detectorTestings[i] else 0
                existing_manday.continuitytesting = int(continuityTestings[i]) if continuityTestings[i] else 0
                existing_manday.programming = int(programmings[i]) if programmings[i] else 0
                existing_manday.continuitytesting1 = int(continuityTestings1[i]) if continuityTestings1[i] else 0
                existing_manday.programming1 = int(programmings1[i]) if programmings1[i] else 0
                existing_manday.chippingplasting = int(chippingPlastings[i]) if chippingPlastings[i] else 0
                existing_manday.handingoverdocument = int(handingOverDocuments[i]) if handingOverDocuments[i] else 0
            else:
                # Insert new record
                new_manday = ManDay(
                    uniquee=uniquee_value,
                    day=int(days[i]) if days[i] else 0,
                    date=dates[i] if dates[i] else '',
                    sdate=sdates[i] if sdates[i] else '',
                    site=sites[i] if sites[i] else '',
                    sub=subs[i] if subs[i] else '',
                    remarks=remarks_list[i] if remarks_list[i] else '',
                    support=supports[i] if supports[i] else '',
                    support1=support1s[i] if support1s[i] else '',
                    cable=int(cables[i]) if cables[i] else 0,
                    pvc=int(pvcs[i]) if pvcs[i] else 0,
                    markingdrilling=int(markingDrillings[i]) if markingDrillings[i] else 0,
                    ci=int(cis[i]) if cis[i] else 0,
                    pvc1=int(pvcs1[i]) if pvcs1[i] else 0,
                    markingdrilling1=int(markingDrillings1[i]) if markingDrillings1[i] else 0,
                    ci1=int(cis1[i]) if cis1[i] else 0,
                    backboxinstallation=int(backboxInstallations[i]) if backboxInstallations[i] else 0,
                    baseinstallation=int(baseInstallations[i]) if baseInstallations[i] else 0,
                    detectorinstallation=int(detectorInstallations[i]) if detectorInstallations[i] else 0,
                    controlmoduleinstallation=int(controlModuleInstallations[i]) if controlModuleInstallations[i] else 0,
                    hooterinstallation=int(hooterInstallations[i]) if hooterInstallations[i] else 0,
                    mcpinstallation=int(mcpInstallations[i]) if mcpInstallations[i] else 0,
                    responseindicatorinstallation=int(responseIndicatorInstallations[i]) if responseIndicatorInstallations[i] else 0,
                    monitormoduleinstallation=int(monitorModuleInstallations[i]) if monitorModuleInstallations[i] else 0,
                    controlrelaymoduleinstallation=int(controlRelayModuleInstallations[i]) if controlRelayModuleInstallations[i] else 0,
                    isolatormoduleinstallation=int(isolatorModuleInstallations[i]) if isolatorModuleInstallations[i] else 0,
                    paspeakerinstallation=int(paSpeakerInstallations[i]) if paSpeakerInstallations[i] else 0,
                    firepanelinstallation=int(firePanelInstallations[i]) if firePanelInstallations[i] else 0,
                    pacontrollerinstallation=int(paControllerInstallations[i]) if paControllerInstallations[i] else 0,
                    smpsinstallation=int(smpsInstallations[i]) if smpsInstallations[i] else 0,
                    detectortesting=int(detectorTestings[i]) if detectorTestings[i] else 0,
                    continuitytesting=int(continuityTestings[i]) if continuityTestings[i] else 0,
                    programming=int(programmings[i]) if programmings[i] else 0,
                    continuitytesting1=int(continuityTestings1[i]) if continuityTestings1[i] else 0,
                    programming1=int(programmings1[i]) if programmings1[i] else 0,
                    chippingplasting=int(chippingPlastings[i]) if chippingPlastings[i] else 0,
                    handingoverdocument=int(handingOverDocuments[i]) if handingOverDocuments[i] else 0,
                    user_id=current_user.id
                )
                db.session.add(new_manday)

        # Commit all changes
        db.session.commit()

        # Redirect to output page after successful submission
        return redirect(url_for('views.outputfas3'))

    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while saving the data.'}), 500
