from django.core.management.base import BaseCommand
from mywebsite.models import Policy, PolicyBenefit  # Update 'accounts' to your actual app name
from faker import Faker
import random
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = "Generate policy benefits for existing policies"

    def handle(self, *args, **kwargs):
        policies = Policy.objects.all()

        if not policies.exists():
            self.stdout.write(self.style.ERROR("❌ No policies found. Please create policies first."))
            return

        benefit_templates = {
            'motor': ['Windscreen Cover', 'Third Party Liability', 'Road Rescue', 'Vehicle Replacement'],
            'health': ['Inpatient Cover', 'Outpatient Cover', 'Dental Cover', 'Optical Cover'],
            'life': ['Death Benefit', 'Disability Benefit', 'Critical Illness Cover'],
            'property': ['Fire Cover', 'Burglary Protection', 'Natural Disaster Cover'],
            'marine': ['Cargo Loss Cover', 'Piracy Protection'],
            'aviation': ['Aircraft Hull Damage', 'Passenger Liability'],
            'liability': ['General Liability', 'Professional Indemnity', 'Product Liability'],
            'travel': ['Medical Evacuation', 'Lost Luggage', 'Trip Cancellation'],
            'agriculture': ['Crop Damage', 'Livestock Loss', 'Drought Cover'],
        }

        count = 0

        for policy in policies:
            category = policy.product.category
            benefit_names = benefit_templates.get(category, ['General Cover'])
            num_benefits = random.randint(1, min(5, len(benefit_names)))

            selected_benefits = random.sample(benefit_names, num_benefits)

            for name in selected_benefits:
                coverage_limit = Decimal(random.randint(1000, int(policy.sum_insured / 2)))
                description = fake.sentence(nb_words=12)

                PolicyBenefit.objects.create(
                    policy=policy,
                    benefit_name=name,
                    coverage_limit=coverage_limit.quantize(Decimal("0.01")),
                    description=description
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"🎉 Created {count} policy benefits for {policies.count()} policies."))
