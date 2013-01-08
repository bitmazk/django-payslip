"""Models for the ``payslip`` application."""
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    """
    Model, which holds general information of a company.

    :name: Name of the company.
    :address: Full address model fields.
    :extra_fields: Custom fields to hold more information.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    address = models.TextField(
        verbose_name=_('Address'),
        blank=True, null=True,
    )

    extra_fields = models.ManyToManyField(
        'payslip.ExtraField',
        verbose_name=_('Extra fields'),
        blank=True, null=True,
    )

    def __unicode__(self):
        return '{0}'.format(self.name)


class Employee(models.Model):
    """
    Model, which holds personal information of employee.

    :user: Connection to the django user model, to allow a login.
    :company: Connection to the employee's company.
    :hr_number: ID to connect some non-digital documents or to use as a
                reference.
    :address: Full address model fields.
    :title: Title of the employee.
    :extra_fields: Custom fields like e.g. confession, tax class.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='employees',
    )

    company = models.ForeignKey(
        'payslip.Company',
        verbose_name=_('Company'),
        related_name='employees',
    )

    hr_number = models.PositiveIntegerField(
        verbose_name=_('HR number'),
        blank=True, null=True,
    )

    address = models.TextField(
        verbose_name=_('Address'),
        blank=True, null=True,
    )

    title = models.CharField(
        max_length=1,
        verbose_name=_('Title'),
        choices=(
            ('1', 'Ms.'),
            ('2', 'Mrs.'),
            ('3', 'Mr.'),
            ('4', 'Dr.'),
        )
    )

    extra_fields = models.ManyToManyField(
        'payslip.ExtraField',
        verbose_name=_('Extra fields'),
        blank=True, null=True,
    )

    is_manager = models.BooleanField(
        default=False,
        verbose_name=_('is Manager'),
    )

    def __unicode__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class ExtraFieldType(models.Model):
    """
    Model to create custom information holders.

    :name: Name of the attribute.
    :description: Description of the attribute.
    :model: Can be set in order to allow the use of only one model.
    :fixed_values: Can transform related exta fields into choices.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )

    model = models.CharField(
        max_length=10,
        choices=(
            ('Employee', 'Employee'),
            ('Payment', 'Payment'),
            ('Company', 'Company'),
        ),
        verbose_name=_('Model'),
        blank=True, null=True,
    )

    fixed_values = models.BooleanField(
        default=False,
        verbose_name=_('Fixed values'),
    )

    def __unicode__(self):
        return '{0}'.format(self.name)


class ExtraField(models.Model):
    """
    Model to create custom fields.

    :field_type: Connection to the field type.
    :value: Current value of this extra field.

    """
    field_type = models.ForeignKey(
        'payslip.ExtraFieldType',
        verbose_name=_('Field type'),
        related_name='extra_fields',
        help_text=_('Only field types with fixed values can be chosen to add'
                    ' global values.'),
    )

    value = models.CharField(
        max_length=200,
        verbose_name=_('Value'),
    )

    def __unicode__(self):
        return '{0} ({1}) - {2}'.format(
            self.field_type, self.field_type.get_model_display() or 'general',
            self.value)


class PaymentType(models.Model):
    """
    Model to create payment types.

    :name: Name of the type.
    :description: Description of the type.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )


class Payment(models.Model):
    """
    Model, which represents one single payment.

    :payment_type: Type of the payment.
    :employee: Connection to the payment receiver.
    :amount: Current amount of the payment.
    :date: Date the payment should accrue.
    :extra_fields: Custom fields like e.g. quantity, bonus.

    """
    payment_type = models.ForeignKey(
        'payslip.PaymentType',
        verbose_name=_('Payment type'),
        related_name='payments',
    )

    employee = models.ForeignKey(
        'payslip.Employee',
        verbose_name=_('Employee'),
        related_name='payments',
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_('Amount'),
    )

    date = models.DateTimeField(
        verbose_name=_('Date'),
        default=now(),
    )

    extra_fields = models.ManyToManyField(
        'payslip.ExtraField',
        verbose_name=_('Extra fields'),
        blank=True, null=True,
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )
