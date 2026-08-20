import unittest
from InventoryManagement import InventoryManagement


class InventoryQA(unittest.TestCase):

    def setUp(self):

        self.inventory = InventoryManagement()

        # Warehouse A
        self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            50
        )

        self.inventory.add_product(
            "Warehouse A",
            "Mouse",
            5
        )

        # Warehouse B
        self.inventory.add_product(
            "Warehouse B",
            "Laptop",
            20
        )

        self.inventory.add_product(
            "Warehouse B",
            "Keyboard",
            30
        )

        # Warehouse C
        self.inventory.add_product(
            "Warehouse C",
            "Laptop",
            100
        )

    # 1. Stock Availability
    def test_stock_availability(self):

        stock = self.inventory.get_stock(
            "Warehouse A",
            "Laptop"
        )

        self.assertEqual(stock, 50)

    # 2. Insufficient Inventory
    def test_insufficient_inventory(self):

        result = self.inventory.remove_product(
            "Warehouse A",
            "Laptop",
            100
        )

        self.assertFalse(result)

        self.assertEqual(
            self.inventory.get_stock(
                "Warehouse A",
                "Laptop"
            ),
            50
        )

    # 3. Warehouse Transfer
    def test_warehouse_transfer(self):

        result = self.inventory.transfer_stock(
            "Warehouse A",
            "Warehouse B",
            "Laptop",
            10
        )

        self.assertTrue(result)

        self.assertEqual(
            self.inventory.get_stock(
                "Warehouse A",
                "Laptop"
            ),
            40
        )

        self.assertEqual(
            self.inventory.get_stock(
                "Warehouse B",
                "Laptop"
            ),
            30
        )

    # 4. Concurrent Orders
    def test_concurrent_orders(self):

        result1 = self.inventory.fulfill_order(
            "Laptop",
            10
        )

        result2 = self.inventory.fulfill_order(
            "Laptop",
            20
        )

        self.assertTrue(result1)
        self.assertTrue(result2)

    # 5. Reorder Threshold
    def test_reorder_threshold(self):

        result = self.inventory.needs_reorder(
            "Warehouse A",
            "Mouse"
        )

        self.assertTrue(result)

    # 6. Invalid Product
    def test_invalid_product(self):

        stock = self.inventory.get_stock(
            "Warehouse A",
            "Mobile"
        )

        self.assertEqual(stock, 0)

    # 7. Negative Inventory
    def test_negative_inventory(self):

        result = self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            -10
        )

        self.assertFalse(result)

    # 8. Multiple Warehouses
    def test_multiple_warehouses(self):

        warehouse = self.inventory.select_warehouse(
            "Laptop",
            25
        )

        # Warehouse A has 50
        # Warehouse B has 20
        # Warehouse C has 100
        #
        # Warehouse B cannot fulfill 25.
        # Warehouse A is selected.

        self.assertEqual(
            warehouse,
            "Warehouse A"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
