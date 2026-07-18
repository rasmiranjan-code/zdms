# apps/core/management/commands/deactivate_expired_batches.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.academics.models import Batch, Enrollment

class Command(BaseCommand):
    help = 'Finds and deactivates batches that have passed their expiry date.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Find batches that are currently active but should be expired
        expired_batches = Batch.objects.filter(is_active=True, expiry_date__lt=today)
        
        if not expired_batches.exists():
            self.stdout.write(self.style.SUCCESS('No batches to expire today.'))
            return

        for batch in expired_batches:
            # Deactivate the batch
            batch.is_active = False
            batch.save()
            
            # Deactivate all enrollments within this batch
            Enrollment.objects.filter(batch=batch).update(is_active=False)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully deactivated batch: {batch}'))