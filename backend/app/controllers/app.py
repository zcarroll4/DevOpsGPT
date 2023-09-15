from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.knowledge.app_info import analyzeService
from app.models.application import Application
from app.models.application_service import ApplicationService
from app.models.application_service_lib import ApplicationServiceLib

bp = Blueprint('app', __name__, url_prefix='/app')


@bp.route('/create', methods=['POST'])
@json_response
def add():
    _ = getI18n("controllers")
    name = request.json.get('app_name')
    tenant_id = session['tenant_id']
    app_id = request.json.get('app_id')
    default_source_branch = request.json.get('app_default_source_branch')
    default_target_branch = request.json.get('app_default_target_branch')
    description = request.json.get('app_description')
    services = request.json.get('service')
    cd_config = request.json.get('app_cd_config')
    ci_config = request.json.get('app_ci_config')
    git_config = request.json.get('app_git_config')
    creater = session['username']

    try:
        if app_id:
            app = Application.update_application(app_id, name=name, description=description, default_source_branch=default_source_branch, default_target_branch=default_target_branch, cd_config=cd_config, ci_config=ci_config, git_config=git_config)
            ApplicationService.delete_service_by_app_id(app_id)
            appID = app_id
        else:
            app = Application.create(tenant_id, creater, name, description, default_source_branch, default_target_branch, git_config, ci_config, cd_config)
            appID = app.app_id

        for service in services:
            if "service_name" in service:
                newService = ApplicationService.create_service(appID, service["service_name"], service["service_git_path"], service["service_workflow"], service["service_role"], service["service_language"], service["service_framework"], service["service_database"], service["service_api_type"], service["service_api_location"], service["service_container_name"], service["service_container_group"], service["service_region"], service["service_public_ip"], service["service_security_group"], service["service_cd_subnet"], service["service_struct_cache"])

            ApplicationServiceLib.create_libs(newService.service_id, service["service_libs_name"])

        return {'success': appID}
    except Exception as e:
        raise Exception(_("Failed to add an application."))


@bp.route('/get', methods=['GET'])
@json_response
def getAll():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']
    appID = request.args.get('app_id')

    try:
        apps = Application.get_all_application(tenantID, appID)

        return {'apps': apps}
    except Exception as e:
        raise Exception(_("Failed to get applications.")) 

@bp.route('/analyze_service', methods=['POST'])
@json_response
def analyze_service():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']
    gitPath = request.json.get('service_git_path')

    info, success = analyzeService(tenantID, gitPath)
    if not success:
        raise Exception(_("Failed to analysis applications.")) 
        
    return info