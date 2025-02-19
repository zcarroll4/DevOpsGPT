from app.extensions import db
from app.models.application_service import ApplicationService

class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    git_config = db.Column(db.Integer, nullable=False)
    ci_config = db.Column(db.Integer, nullable=False)
    cd_config = db.Column(db.Integer, nullable=False)
    creater = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    default_source_branch = db.Column(db.String(255))
    default_target_branch = db.Column(db.String(255))

    def create(tenant_id, creater, name, description, default_source_branch, default_target_branch, git_config, ci_config, cd_config):
        if not tenant_id:
            tenant_id = 0

        app = Application(
            tenant_id=tenant_id,
            creater=creater,
            name=name,
            git_config=git_config, 
            ci_config=ci_config, 
            cd_config=cd_config,
            description=description,
            default_source_branch=default_source_branch,
            default_target_branch=default_target_branch
        )
        db.session.add(app)
        db.session.commit()
        return app

    @staticmethod
    def get_all_application(tenant_id, appID):
        applications = Application.query.order_by(Application.app_id.desc()).all()
        if appID:
            applications = Application.query.order_by(Application.app_id.desc()).filter_by(app_id=appID).all()
        else:
            applications = Application.query.order_by(Application.app_id.desc()).filter_by(tenant_id=tenant_id).all()

        application_list = []
        
        for app in applications:
            app_dict = {
                'app_id': app.app_id,
                'tenant_id': app.tenant_id,
                'creater': app.creater,
                'name': app.name,
                'git_config': app.git_config,
                'ci_config': app.ci_config,
                'cd_config': app.cd_config,
                'description': app.description,
                'default_source_branch': app.default_source_branch,
                'default_target_branch': app.default_target_branch,
                'service': ApplicationService.get_services_by_app_id(app.app_id)
            }
            application_list.append(app_dict)
        
        return application_list

    def get_application_by_id(appID):
        app = Application.query.get(appID)
        app_dict = {
                'app_id': app.app_id,
                'tenant_id': app.tenant_id,
                'creater': app.creater,
                'name': app.name,
                'git_config': app.git_config,
                'ci_config': app.ci_config,
                'cd_config': app.cd_config,
                'description': app.description,
                'default_source_branch': app.default_source_branch,
                'default_target_branch': app.default_target_branch,
                'service': ApplicationService.get_services_by_app_id(app.app_id)
            }
        return app_dict
    
    def update_application(app_id, **kwargs):
        app = Application.query.get(app_id)
        if app:
            for key, value in kwargs.items():
                setattr(app, key, value)
            db.session.commit()
            return app
        return None
