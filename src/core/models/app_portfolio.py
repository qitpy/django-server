from django.db import models

class PortfolioMessage(models.Model):
    """Message send from user on Portfolio_Page"""
    message = models.TextField(blank=False, null=False)
    ip_address = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'portfolio_message'


class PortfolioAccessFrequency(models.Model):
    """number of access by times"""
    ip_address = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_access_frequency'


