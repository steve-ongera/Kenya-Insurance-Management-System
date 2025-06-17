from django import template

register = template.Library()

@register.filter
def claim_status_color(status):
    color_map = {
        'reported': 'warning',
        'investigating': 'info',
        'processing': 'primary',
        'approved': 'success',
        'declined': 'danger',
        'settled': 'secondary',
        'closed': 'dark'
    }
    return color_map.get(status, 'secondary')

@register.filter
def payment_status_color(status):
    color_map = {
        'pending': 'warning',
        'completed': 'success',
        'failed': 'danger',
        'cancelled': 'secondary',
        'refunded': 'info'
    }
    return color_map.get(status, 'secondary')
