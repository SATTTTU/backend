from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title
    
class brand(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title
    
class Sub_category(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title +"......" + self.category.title
    

Availability_fields = (
    ('In Stock', 'In Stock'),
    ('Out of Stock', 'Out of Stock'),
    ('Pre-Order', 'Pre-Order'),
    

      
  )
class Product(models.Model):
    image = models.ImageField(upload_to="products",blank=True,null=True)
    image2 = models.ImageField(upload_to="products",blank=True,null=True)
    image3 = models.ImageField(upload_to="products",blank=True,null=True)
     
    name = models.CharField(max_length=200)
    categoroy = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(brand,on_delete=models.CASCADE,null=True,blank=True)
    availability = models.CharField(max_length=15, choices=Availability_fields,null=True,blank=True)
    subcategory = models.ForeignKey(Sub_category,on_delete=models.CASCADE)
    desc = RichTextField(blank=True)
    mark_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_percentages = models.DecimalField(max_digits=4,decimal_places=2)
    price = models.DecimalField(max_digits=10,decimal_places=2,editable=False)

    def save(self,*args, **kwargs):

        self.price = self.mark_price*(1-self.discount_percentages/100)
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.name
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_picture",null=True,blank=True)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.user.username
    
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name