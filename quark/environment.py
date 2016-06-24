# Copyright (c) 2015 Rackspace Hosting Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron._i18n import _
from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF


class Capabilities(object):
    SECURITY_GROUPS = "security_groups"
    EGRESS = "egress"
    TENANT_NETWORK_SG = "tenant_network_sg"
    IP_BILLING = "ip_billing"
    SG_UPDATE_ASYNC = "security_groups_update_async"


quark_opts = [
    cfg.ListOpt("environment_capabilities",
                default=",".join([Capabilities.SECURITY_GROUPS]),
                help=_("Capabilities supported by a given environment's"
                       "deployment.")),
]


CONF.register_opts(quark_opts, "QUARK")
LOG = logging.getLogger(__name__)


class has_capability(object):
    def __init__(self, capability):
        self.capability = capability

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            if self.capability in CONF.QUARK.environment_capabilities:
                return f(*args, **kwargs)
        return wrapped
