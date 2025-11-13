from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, time
from decimal import Decimal, ROUND_UP

class User(AbstractUser):
    """ขยาย Django User Model"""
    ROLE_CHOICES = [
        ('user', 'ผู้ใช้ทั่วไป'),
        ('admin', 'ผู้ดูแลระบบ'),
    ]
    
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    image = models.ImageField(upload_to='sport_fields/', blank=True, null=True, verbose_name='รูปภาพ')
    
    def __str__(self):
        return self.username


class SportField(models.Model):
    """สนามกีฬา"""
    SPORT_TYPES = [
        ('football', 'ฟุตบอล'),
        ('futsal', 'ฟุตซอล'),
        ('basketball', 'บาสเกตบอล'),
        ('volleyball', 'วอลเลย์บอล'),
        ('badminton', 'แบดมินตัน'),
        ('tennis', 'เทนนิส'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'พร้อมใช้งาน'),
        ('maintenance', 'ปิดปรับปรุง'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='ชื่อสนาม')
    sport_type = models.CharField(max_length=20, choices=SPORT_TYPES, verbose_name='ประเภทกีฬา')
    description = models.TextField(blank=True, verbose_name='รายละเอียด')
    capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='ความจุ (คน)')
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='ราคา/ชม.')
    image = models.ImageField(upload_to='sport_fields/', blank=True, null=True, verbose_name='รูปภาพ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='สถานะ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'สนามกีฬา'
        verbose_name_plural = 'สนามกีฬา'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_sport_type_display()})"


class Booking(models.Model):
    """การจองสนาม"""
    STATUS_CHOICES = [
        ('pending', 'รอยืนยัน'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('cancelled', 'ยกเลิก'),
        ('completed', 'เสร็จสิ้น'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='ผู้จอง')
    sport_field = models.ForeignKey(SportField, on_delete=models.CASCADE, related_name='bookings', verbose_name='สนาม')
    booking_date = models.DateField(verbose_name='วันที่จอง')
    start_time = models.TimeField(verbose_name='เวลาเริ่มต้น')
    end_time = models.TimeField(verbose_name='เวลาสิ้นสุด')
    hours = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='จำนวนชั่วโมง')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ราคารวม')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='สถานะ')
    note = models.TextField(blank=True, verbose_name='หมายเหตุ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    