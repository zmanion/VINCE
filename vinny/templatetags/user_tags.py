#########################################################################
# VINCE
#
# Copyright 2022 Carnegie Mellon University.
#
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING
# INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON
# UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED,
# AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR
# PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE
# MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND
# WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
#
# Released under a MIT (SEI)-style license, please see license.txt or contact
# permission@sei.cmu.edu for full terms.
#
# [DISTRIBUTION STATEMENT A] This material has been approved for public
# release and unlimited distribution.  Please see Copyright notice for non-US
# Government use and distribution.
#
# Carnegie Mellon®, CERT® and CERT Coordination Center® are registered in the
# U.S. Patent and Trademark Office by Carnegie Mellon University.
#
# This Software includes and/or makes use of Third-Party Software each subject
# to its own license.
#
# DM21-1126
########################################################################
from django import template
from vinny.permissions import is_in_group_vincetrack, is_in_group_vincelimited, is_in_group_vincegroupadmin

register = template.Library()

@register.filter
def limited(user):
    return (is_in_group_vincetrack(user) or is_in_group_vincelimited(user))

@register.filter
def trackuser(user):
    return is_in_group_vincetrack(user)

@register.filter
def groupadmin(user, contact):
    try:
        from vinny.models import VinceCommGroupAdmin
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in template tags: Can't load VinceCommGroupAdmin model.")
    return (is_in_group_vincegroupadmin(user) and VinceCommGroupAdmin.objects.filter(contact=contact, email__email=user.email).exists())


@register.filter
def case_access(cases, user):
    cases = cases.filter(user=user).values_list('casemember__case__vuid', flat=True)
    return list(cases)


@register.filter
def notify_emails(user, contact):
    try:
        from vinny.models import VinceCommEmail
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in template tags: Can't load VinceCommEmail.")
    email = VinceCommEmail.objects.filter(email=user.email, contact=contact).first()
    if email:
        if email.email_function in ["TO", "CC"]:
            return True
        else:
            return False
    return False
    
    
