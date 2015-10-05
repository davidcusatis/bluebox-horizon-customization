from django.utils.translation import ugettext_lazy as _

import horizon

# expose host aggregates to cloud_admin
# default permissions for admin_dashboard _should_ be ('openstack.roles.admin',)
# so we want to append our cloud_admin role to the first tuple
# https://github.com/openstack/django_openstack_auth/blob/master/openstack_auth/user.py#L376
# (('openstack.roles.admin', 'openstack.roles.cloud_admin',),) == logcal OR
admin_dashboard = horizon.get_dashboard("admin")
permissions = list(getattr(admin_dashboard, 'permissions', []))
permissions[0] = (permissions[0],) + ('openstack.roles.cloud_admin',)

# set admin dashboard visible to both admin, and cloud_admin
admin_dashboard.permissions = tuple(permissions)

#expose aggregates to cloud_admin
aggregates = admin_dashboard.get_panel('aggregates')
aggregates_permissions = list(getattr(aggregates, 'permissions', []))

# aggregates perms already has admin, it's a similar case as with the dashboard
aggregates_permissions[0] = (aggregates_permissions[0],) + \
                            ('openstack.roles.cloud_admin',)
aggregates.permissions = tuple(aggregates_permissions)

# hide all other admin panels from cloud_admin
admin_panels_to_remove = ['defaults', 'flavors', 'images', 'info', 'networks',
                        'routers', 'volumes']
for p in admin_panels_to_remove:
    panel = admin_dashboard.get_panel(p)
    panel_permissions = list(getattr(panel, 'permissions', []))
    panel_permissions.append('openstack.roles.admin')
    panel.permissions = tuple(panel_permissions)


# hide identity/domains panel from non full admins
identity_dashboard = horizon.get_dashboard('identity')
domains = identity_dashboard.get_panel('domains')
domains_permissions = list(getattr(domains, 'permissions', []))
domains_permissions.append('openstack.roles.admin')
domains.permissions = tuple(domains_permissions)

# hide project/stacks/resource types panel from non full admins
project_dashboard = horizon.get_dashboard('project')
resource_types = project_dashboard.get_panel('stacks.resource_types')
resource_type_permissions = list(getattr(resource_types, 'permissions', []))
resource_type_permissions.append('openstack.roles.admin')
resource_types.permissions = tuple(resource_type_permissions)
