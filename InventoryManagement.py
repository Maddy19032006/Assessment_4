class InventoryManagement:

    def __init__(self):
        # Multiple warehouses
        self.warehouses = {
            "Warehouse A": {},
            "Warehouse B": {},
            "Warehouse C": {}
        }

        # Reorder threshold
        self.reorder_threshold = 10

    # Add product
    def add_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if quantity < 0:
            return False

        if product not in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] = quantity
        else:
            self.warehouses[warehouse][product] += quantity

        return True

    # Remove product
    def remove_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if product not in self.warehouses[warehouse]:
            return False

        if quantity <= 0:
            return False

        if self.warehouses[warehouse][product] < quantity:
            return False

        self.warehouses[warehouse][product] -= quantity

        return True

    # Check stock availability
    def get_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return None

        return self.warehouses[warehouse].get(product, 0)

    # Transfer stock
    def transfer_stock(self, source, destination, product, quantity):

        if source not in self.warehouses:
            return False

        if destination not in self.warehouses:
            return False

        if source == destination:
            return False

        if quantity <= 0:
            return False

        if self.get_stock(source, product) < quantity:
            return False

        self.warehouses[source][product] -= quantity

        if product not in self.warehouses[destination]:
            self.warehouses[destination][product] = 0

        self.warehouses[destination][product] += quantity

        return True

    # Reorder check
    def needs_reorder(self, warehouse, product):

        stock = self.get_stock(warehouse, product)

        if stock is None:
            return False

        return stock <= self.reorder_threshold

    # Low stock detection
    def low_stock_products(self, warehouse):

        if warehouse not in self.warehouses:
            return []

        low_stock = []

        for product, quantity in self.warehouses[warehouse].items():

            if quantity <= self.reorder_threshold:
                low_stock.append(product)

        return low_stock

    # Warehouse selection
    # Automatically identifies the warehouse
    # from which an order should be fulfilled.
    def select_warehouse(self, product, quantity):

        if quantity <= 0:
            return None

        available_warehouses = []

        for warehouse in self.warehouses:

            stock = self.get_stock(warehouse, product)

            if stock >= quantity:
                available_warehouses.append(
                    (warehouse, stock)
                )

        if not available_warehouses:
            return None

        # Select warehouse having the lowest
        # sufficient stock so that excess stock
        # is not unnecessarily used.
        available_warehouses.sort(
            key=lambda x: x[1]
        )

        return available_warehouses[0][0]

    # Fulfill order
    def fulfill_order(self, product, quantity):

        warehouse = self.select_warehouse(
            product,
            quantity
        )

        if warehouse is None:
            return False

        self.warehouses[warehouse][product] -= quantity

        return True
