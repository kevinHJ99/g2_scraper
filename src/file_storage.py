import os
import json
import csv

class FileStorageManager:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        self.products = []
        self.links = set()

        os.makedirs(self.output_dir, exist_ok=True)

    def add_products(self, products, category):
        for product in products:

            link = product.get('link')
            if link and link not in self.links:
                product['category'] = category
                self.products.append(product)
                self.links.add(link)

    def save_json(self, filename='products.json'):
        path = os.path.join(self.output_dir, filename)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving JSON file: {e}")

    def save_csv(self, filename='products.csv'):
        path = os.path.join(self.output_dir, filename)
        
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'description', 'ratings', 'seller', 'link', 'category'])
                writer.writeheader()
                writer.writerows(self.products)
        except Exception as e:
            print(f"Error saving CSV file: {e}")

    def get_stats(self):
        """Get storage statistics."""
        return {
            "total_products": len(self.products),
            "unique_links": len(self.links),
            "categories": len(set(p.get('category') for p in self.products))
        }