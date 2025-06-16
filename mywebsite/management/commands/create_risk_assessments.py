from django.core.management.base import BaseCommand
from mywebsite.models import RiskAssessment, Policy  # Adjust path to your models
from faker import Faker
from decimal import Decimal
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate risk assessments for policies"

    def handle(self, *args, **kwargs):
        motor_policies = Policy.objects.filter(product__category='motor')

        if not motor_policies.exists():
            self.stdout.write(self.style.ERROR("❌ No motor policies found."))
            return

        created = 0

        for policy in motor_policies:
            if hasattr(policy, 'risk_assessment'):
                continue  # Skip if already has assessment

            vehicle_make = random.choice(['Toyota', 'Nissan', 'Honda', 'Ford', 'Subaru'])
            vehicle_model = fake.word().capitalize()
            vehicle_year = random.randint(2000, 2023)
            vehicle_value = Decimal(random.randint(300000, 3000000))
            driver_age = random.randint(21, 65)
            driving_experience = max(driver_age - 18, 1)
            previous_claims = random.choice([0, 0, 0, 1, 2])

            # Simple risk score logic
            base_score = Decimal(50)
            if previous_claims > 0:
                base_score += Decimal(previous_claims * 10)
            if driver_age < 25 or driver_age > 60:
                base_score += Decimal(10)
            if vehicle_value > 2000000:
                base_score += Decimal(5)

            risk_score = base_score.quantize(Decimal("0.01"))
            risk_category = (
                'low' if risk_score < 40 else
                'medium' if risk_score <= 70 else
                'high'
            )

            RiskAssessment.objects.create(
                policy=policy,
                vehicle_make=vehicle_make,
                vehicle_model=vehicle_model,
                vehicle_year=vehicle_year,
                vehicle_value=vehicle_value,
                registration_number=fake.bothify(text='K?? ###X'),
                engine_number=fake.bothify(text='ENG#####'),
                chassis_number=fake.bothify(text='CHS#####'),
                driver_age=driver_age,
                driving_experience=driving_experience,
                previous_claims=previous_claims,
                risk_score=risk_score,
                risk_category=risk_category,
                medical_report_required=random.choice([False, True]),
                property_inspection_required=random.choice([False, True]),
                additional_requirements=fake.text(max_nb_chars=100) if random.choice([False, True]) else ''
            )

            self.stdout.write(self.style.SUCCESS(
                f"✅ Risk assessment created for policy {policy.policy_number} [{risk_category}]"
            ))
            created += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Created {created} risk assessments."))
