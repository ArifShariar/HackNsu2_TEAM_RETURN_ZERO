from django.db import models
from login_signup import models as md

# Create your models here.
class vendor_product_categories(models.Model):
    category_name = models.CharField(max_length=50, null=False, unique=True)
    rank = models.IntegerField(null=True)

    def __str__(self):
        return self.category_name

class vendor_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    price = models.CharField(max_length=30, null=True)
    category_fk = models.ForeignKey(vendor_product_categories, on_delete=models.DO_NOTHING, null=True)
    vendor_fk = models.ForeignKey(md.Vendor, on_delete=models.CASCADE, null=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name

class company_product(models.Model):
    name = models.CharField(max_length=30)

    price = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)


    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + "( Stock :"+str(self.stock)+" Price :"+str(self.price)+")"

class order(models.Model):
    order_time = models.DateField()
    order_amount = models.IntegerField(null=True)
    status = models.CharField(max_length=30 , default='Pending')
    customer_fk = models.ForeignKey(md.Customer , on_delete=models.DO_NOTHING, null=True)
    product_fk = models.ForeignKey(company_product, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.customer_fk.user.username + " amount: "+ str(self.order_amount)
        #return " amount: "+ str(self.order_amount)

class notification(models.Model):
    noti_msg = models.CharField(max_length=1000)
    type = models.CharField(max_length=200, null=True, choices=[("Demand", "Possible Rise in Demand Soon"), ("Bid Success", "Your Bid Has Been Accepted by Company A"), ("Relevant Bid", "Company A Has Posted A Requirement which might Interest you")])
    vendor_fk = models.ManyToManyField(md.Vendor , blank=True)
    issue_date = models.DateField(null=True)

    def __str__(self):
        return self.noti_msg

class raw_material_requirments(models.Model):
    description = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=50)
    category_fk = models.ForeignKey(vendor_product_categories, on_delete=models.DO_NOTHING, null=True)
    issue_date = models.DateField(null=True)
    vendor_fk = models.ForeignKey(md.Vendor, on_delete=models.DO_NOTHING, null=True, blank=True)
    bids = models.ManyToManyField(md.Vendor, related_name="bids", blank = True)

    def __str__(self):
        return self.description[:min(120, len(self.description))]

class bid_details(models.Model):
    proposal = models.CharField(max_length=1000)
    vendor_fk = models.ForeignKey(md.Vendor, on_delete=models.CASCADE)
    req_fk = models.ForeignKey(raw_material_requirments, on_delete=models.CASCADE)

    def __str__(self):
        return self.proposal
