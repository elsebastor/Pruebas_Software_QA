import unittest
from hotels import Hotel, Customer, Reservation, Persistent, int_validation, str_validation, hotel_cli, customer_cli, reservation_cli, main 
import os
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock


class TestPersistent(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for test files."""
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)  # Ensure cleanup after tests
        Persistent.data_folder = self.temp_dir.name  # Use the temp directory for tests

    def test_file_creation(self):
        """Test if the file is created if it does not exist."""
        test_filename = 'test_file.json'
        _ = Persistent(test_filename)  # Initialization should create the file
        expected_path = os.path.join(Persistent.data_folder, test_filename)
        self.assertTrue(os.path.isfile(expected_path), "The file was not created.")

    def test_read_write_data(self):
        """Test writing to and reading from a file."""
        test_filename = 'test_data.json'
        test_data = [{'name': 'Test', 'value': 123}, {'name': 'Test 2', 'value': 456}]
        persistent = Persistent(test_filename)
        persistent.write_data(test_data)
        read_data = persistent.read_data()
        self.assertEqual(test_data, read_data, "The read data does not match the written data.")

class TestValidationFunctions(unittest.TestCase):

    def test_int_validation(self):
        # Test valid integers
        self.assertTrue(int_validation(10))
        self.assertTrue(int_validation(0))
        self.assertTrue(int_validation(-10))

        # Test integer with range
        self.assertTrue(int_validation(5))
        self.assertTrue(int_validation(11))

        # Test invalid types
        self.assertFalse(int_validation("10"))
        self.assertFalse(int_validation(10.1))
        self.assertFalse(int_validation(None))

    def test_str_validation(self):
        # Test valid strings
        self.assertTrue(str_validation("test"))

        # Test invalid types
        self.assertFalse(str_validation(100))
        self.assertFalse(str_validation([1, 2, 3]))
        self.assertFalse(str_validation(None))

class TestHotel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hotel = Hotel()

    def test_create_hotel(self):
        """Test creating a hotel successfully."""
        self.hotel.create_hotel(1, "Test Hotel", "Test Location", 100)
        self.hotel.create_hotel(2, "Test Hotel", "Test Location", 100)
        self.hotel.create_hotel(1, "Test Hotel", 123, 100)
        self.hotel.create_hotel(1, 123, "Test Location", 100)
        self.hotel.create_hotel(1, "Test Hotel", "Test Location", "invalid_rooms")
        self.hotel.create_hotel("invalid_id", "Test Hotel", "Test Location", 100)

    def test_delete_hotel(self):
        self.hotel.delete_hotel(1)
        self.hotel.delete_hotel("asfs")

    def test_display_hotel(self):
        self.hotel.display_hotel(2)
        self.hotel.display_hotel("dfgda")
        self.hotel.display_hotel(54654354565)

    def test_modify_hotel(self):
        self.hotel.modify_hotel(2, "Test Hotel", "Test change", 100)
        self.hotel.modify_hotel("545df", "Test Hotel", "Test change", 100)
        self.hotel.modify_hotel(5465435454565)

    def test_reserve_room(self):
        self.hotel.reserve_room(1, 2, 3, 100)
        self.hotel.reserve_room("dsf", 2, 3, 100)
        self.hotel.reserve_room(1, "hgbdf", 3, 100)
        self.hotel.reserve_room(1, 2, "dsff", 100)
        self.hotel.reserve_room(1, 2, 3, "sffd")
        self.hotel.reserve_room(1, 2, 3, 100)

    def test_cancel_reservation(self):
        self.hotel.cancel_reservation(1)
        self.hotel.cancel_reservation("dsf")


class TestCustomer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hotel = Customer()

    def test_create_customer(self):
        self.hotel.create_customer(1, "Test Hotel", "Test Location")
        self.hotel.create_customer("dsf", "Test Hotel", "Test Location")
        self.hotel.create_customer(2, 555, "Test Location")
        self.hotel.create_customer(2, "Test Hotel", 24244)
        self.hotel.create_customer(2, "Test Hotel", "Test Location")

    def test_delete_customer(self):
        self.hotel.delete_customer(1)
        self.hotel.delete_customer("dsdfds")

    def test_display_customer(self):
        self.hotel.display_customer(2)
        self.hotel.display_customer("dsfdsf")
        self.hotel.display_customer(546545)

    def test_modify_customer(self):
        self.hotel.modify_customer(2, "Testsxdf Hotel", "Test Location")
        self.hotel.modify_customer("7ddfs", "Testsxdf Hotel", "Test Location")
        self.hotel.modify_customer(54654, "Testsxdf Hotel", "Test Location")

class TestReservation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hotel = Reservation()

    def test_create_reservation(self):
        self.hotel.create_reservation(1, 1, 1, 100,"2023-02-01","2023-03-02")
        self.hotel.create_reservation("sfd", 1, 1, 100,"2023-02-01","2023-03-02")
        self.hotel.create_reservation(1, "dsfsd", 1, 100,"2023-02-01","2023-03-02")
        self.hotel.create_reservation(1, 1, 1, "sfffs","2023-02-01","2023-03-02")
        self.hotel.create_reservation(1, 1, 1, 100,121,"2023-03-02")
        self.hotel.create_reservation(1, 1, 1, 100,"121",54)
        self.hotel.create_reservation(1, 1, "dfsd", 100,"121",54)
        self.hotel.create_reservation(3, 1, 1, 100,"121",54)

    def test_cancel_reservation(self):
        self.hotel.cancel_reservation(1)
        self.hotel.cancel_reservation("425")
        self.hotel.cancel_reservation(3)

class TestCLI(unittest.TestCase):
    @patch('builtins.print')  # Mocks the print function
    @patch('builtins.input', side_effect=['1'])  # Mocks the input function to simulate user inputs
    @patch('hotels.hotel_cli')  # Mocks the hotel_cli function
    def test_hotel_choice(self, mock_hotel_cli, mock_input, mock_print):
        """
        Test that choosing '1' calls hotel_cli function and then exits on choosing '4'.
        """
        main()
        mock_hotel_cli.assert_called_once()  # Assert hotel_cli was called

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['2',"1"])
    @patch('hotels.customer_cli')
    def test_customer_choice(self, mock_customer_cli, mock_input, mock_print):
        """
        Test that choosing '2' calls customer_cli function and then exits on choosing '4'.
        """
        main()
        mock_customer_cli.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['3',"4"])
    @patch('hotels.reservation_cli')
    def test_reservation_choice(self, mock_reservation_cli, mock_input, mock_print):
        """
        Test that choosing '3' calls reservation_cli function and then exits on choosing '4'.
        """
        main()
        mock_reservation_cli.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['4',"6"])
    def test_exit_choice(self, mock_input, mock_print):
        """
        Test that choosing '4' exits the program.
        """
        with self.assertRaises(SystemExit):  # Assuming your main function calls sys.exit to exit
            main()
        assert "Exiting the program." in str(mock_print.call_args)

        # This test ensures the main navigation loop works as expected.
        # You could add more specific assertions here based on the operations performed.


class TestReservationCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['3'])  # Simulates choosing to exit the reservation manager
    @patch('builtins.print')
    def test_exit_reservation_menu(self, mock_print, mock_input):
        reservation_manager = MagicMock()
        reservation_cli(reservation_manager)
        mock_print.assert_called_with("\nReservation Management:")
    
    @patch('builtins.input', side_effect=['1', 'res_id', 'cust_id', 'hotel_id', 'room_num', '2023-01-01', '2023-01-05', '3'])
    @patch('builtins.print')
    def test_create_reservation(self, mock_print, mock_input):
        reservation_manager = MagicMock()
        reservation_cli(reservation_manager)
        reservation_manager.create_reservation.assert_called_once_with('res_id', 'cust_id', 'hotel_id', 'room_num', '2023-01-01', '2023-01-05')
    
    @patch('builtins.input', side_effect=['2', 'res_id', '3'])
    @patch('builtins.print')
    def test_cancel_reservation(self, mock_print, mock_input):
        reservation_manager = MagicMock()
        reservation_cli(reservation_manager)
        reservation_manager.cancel_reservation.assert_called_once_with('res_id')
    
    @patch('builtins.input', side_effect=['4', '3'])  # Simulates choosing an invalid option and then exiting
    @patch('builtins.print')
    def test_invalid_choice(self, mock_print, mock_input):
        reservation_manager = MagicMock()
        reservation_cli(reservation_manager)
        mock_print.assert_any_call("Invalid choice. Please try again.")

class TestCustomerCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['5'])  # Simulates choosing to exit the customer manager
    @patch('builtins.print')
    def test_exit_customer_menu(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        mock_print.assert_called_with("\nCustomer Management:")
    
    @patch('builtins.input', side_effect=['1', 'cust_id', 'John Doe', 'john.doe@example.com', '5'])
    @patch('builtins.print')
    def test_create_customer(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        customer_manager.create_customer.assert_called_once_with('cust_id', 'John Doe', 'john.doe@example.com')
    
    @patch('builtins.input', side_effect=['2', 'cust_id', '5'])
    @patch('builtins.print')
    def test_delete_customer(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        customer_manager.delete_customer.assert_called_once_with('cust_id')
    
    @patch('builtins.input', side_effect=['3', 'cust_id', '5'])
    @patch('builtins.print')
    def test_display_customer_information(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        customer_manager.display_customer.assert_called_once_with('cust_id')
    
    @patch('builtins.input', side_effect=['4', 'cust_id', 'Jane Doe', 'jane.doe@example.com', '5'])
    @patch('builtins.print')
    def test_modify_customer_information(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        customer_manager.modify_customer.assert_called_once_with('cust_id', 'Jane Doe', 'jane.doe@example.com')

    @patch('builtins.input', side_effect=['6', '5'])  # Simulates choosing an invalid option and then exiting
    @patch('builtins.print')
    def test_invalid_choice(self, mock_print, mock_input):
        customer_manager = MagicMock()
        customer_cli(customer_manager)
        mock_print.assert_any_call("Invalid choice. Please try again.")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestHotel))
    suite.addTest(unittest.makeSuite(TestCustomer))
    suite.addTest(unittest.makeSuite(TestReservation))
    suite.addTest(unittest.makeSuite(TestPersistent))
    suite.addTest(unittest.makeSuite(TestValidationFunctions))
    suite.addTest(unittest.makeSuite(TestCLI))
    suite.addTest(unittest.makeSuite(TestCustomerCLI))
    suite.addTest(unittest.makeSuite(TestReservationCLI))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
