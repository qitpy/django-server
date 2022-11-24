from django.db import models


class PortfolioMessage(models.Model):
    """Message send from user on Portfolio_Page"""
    message = models.TextField(blank=False, null=False)
    name_or_email = models.TextField(blank=True, null=True)
    ip_address = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_message'

    def __str__(self):
        return f"PortfolioMessage[" \
               f"{self.message}," \
               f"{self.name_or_email}," \
               f"{self.ip_address}," \
               f"{self.created_at}]"


class PortfolioAccessFrequency(models.Model):
    """number of access by times"""
    ip_address = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_access_frequency'

    def __str__(self):
        return self.ip_address
