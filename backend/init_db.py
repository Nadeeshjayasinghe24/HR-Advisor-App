from src.main import app, db, SubscriptionPlan

with app.app_context():
    db.drop_all()
    db.create_all()

    # Initialize default subscription plans if they don't exist
    if not SubscriptionPlan.query.first():
        db.session.add(SubscriptionPlan(name='Free', monthly_cost=0, coin_allocation=10, features='HR Advice,Basic Templates'))
        db.session.add(SubscriptionPlan(name='Premium', monthly_cost=29.99, coin_allocation=500, features='All HR Advice,Advanced Templates,Workflow Automation'))
        db.session.add(SubscriptionPlan(name='Enterprise', monthly_cost=99.99, coin_allocation=2000, features='All Features,Dedicated Support,Custom Integrations'))
        db.session.commit()
    print("Database initialized and subscription plans added.")

