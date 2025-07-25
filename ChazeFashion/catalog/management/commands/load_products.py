import csv
import os
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Product  # Import your Product model


class Command(BaseCommand):
    help = 'Loads products from a specified CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing product data.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')

        self.stdout.write(self.style.NOTICE(f'Attempting to load products from: {csv_file_path}'))

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                required_headers = ['pr_name', 'pr_price', 'pr_cate', 'pr_stk_quant']
                if not all(header in reader.fieldnames for header in required_headers):
                    raise CommandError(f"CSV must contain the following headers: {', '.join(required_headers)}")

                products_created = 0
                products_updated = 0

                valid_categories = [choice[0] for choice in Product.CATEGORY_CHOICES]

                for row_num, row in enumerate(reader, 1):
                    try:
                        pr_name = row.get('pr_name', '').strip()
                        pr_price_str = row.get('pr_price', '').strip()
                        pr_cate = row.get('pr_cate', '').strip()
                        pr_description = row.get('pr_description', '').strip()
                        pr_stk_quant_str = row.get('pr_stk_quant', '').strip()
                        pr_images_path = row.get('pr_images', '').strip()

                        pr_reviews_str = row.get('pr_reviews', '0').strip()
                        pr_buy_quant_str = row.get('pr_buy_quant', '0').strip()
                        pr_dimensions = row.get('pr_dimensions', '').strip()
                        pr_weights = row.get('pr_weights', '').strip()
                        pr_offers = row.get('pr_offers', '').strip()
                        pr_season = row.get('pr_season', 'All Season').strip()
                        pr_fabric = row.get('pr_fabric', '').strip()
                        pr_texture = row.get('pr_texture', '').strip()
                        pr_brand = row.get('pr_brand', '').strip()

                        if not pr_name or not pr_price_str or not pr_cate or not pr_stk_quant_str:
                            self.stderr.write(self.style.WARNING(f"Skipping row {row_num}: Missing required data."))
                            continue

                        if pr_cate not in valid_categories:
                            self.stderr.write(self.style.WARNING(
                                f"Skipping row {row_num} for '{pr_name}': Invalid category '{pr_cate}'."))
                            continue

                        try:
                            pr_price = float(pr_price_str)
                            pr_stk_quant = int(pr_stk_quant_str)
                            pr_reviews = float(pr_reviews_str)
                            pr_buy_quant = int(pr_buy_quant_str)
                        except ValueError:
                            self.stderr.write(self.style.ERROR(
                                f"Skipping row {row_num} for '{pr_name}': Invalid number format."))
                            continue

                        image_field_value = pr_images_path if pr_images_path else None

                        product, created = Product.objects.update_or_create(
                            pr_name=pr_name,
                            defaults={
                                'pr_price': pr_price,
                                'pr_cate': pr_cate,
                                'pr_description': pr_description,
                                'pr_stk_quant': pr_stk_quant,
                                'pr_images': image_field_value,
                                'pr_reviews': pr_reviews,
                                'pr_buy_quant': pr_buy_quant,
                                'pr_dimensions': pr_dimensions,
                                'pr_weights': pr_weights,
                                'pr_offers': pr_offers,
                                'pr_season': pr_season,
                                'pr_fabric': pr_fabric,
                                'pr_texture': pr_texture,
                                'pr_brand': pr_brand,
                            }
                        )

                        if created:
                            products_created += 1
                            self.stdout.write(self.style.SUCCESS(f'Created product: {product.pr_name}'))
                        else:
                            products_updated += 1
                            self.stdout.write(self.style.SUCCESS(f'Updated product: {product.pr_name}'))

                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error processing row {row_num} ({pr_name}): {e}"))

            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded products. Created: {products_created}, Updated: {products_updated}.'))

        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
