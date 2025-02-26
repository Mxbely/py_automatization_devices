import pytest
from unittest.mock import patch
from testing.scanner_handler import CheckQr


class TestCheckQr:
    @pytest.mark.parametrize(
        "qr, expected_color",
        [
            pytest.param("123", "Red", id="QR length 3"),
            pytest.param("12345", "Green", id="QR length 5"),
            pytest.param("1234567", "Fuzzy Wuzzy", id="QR length 7"),
        ],
    )
    @patch.object(CheckQr, "check_in_db", return_value=True)
    def test_positive_check_len_color(self, mock_db, qr, expected_color):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        assert checker.color == expected_color

    @pytest.mark.parametrize(
        "qr, expected_color",
        [
            pytest.param("1", None, id="QR length 1"),
            pytest.param("12", None, id="QR length 2"),
            pytest.param("1234", None, id="QR length 4"),
            pytest.param("123456", None, id="QR length 6"),
            pytest.param("12345678", None, id="QR length 8"),
        ],
    )
    @patch.object(CheckQr, "check_in_db", return_value=True)
    def test_not_existing_color(self, mock_db, qr, expected_color):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        assert checker.color == expected_color

    @pytest.mark.parametrize(
        "qr, exepted_error",
        [
            pytest.param("123", ConnectionError, id="QR length 3"),
            pytest.param("12345", ConnectionError, id="QR length 5"),
            pytest.param("1234567", ConnectionError, id="QR length 7"),
            pytest.param("1", ConnectionError, id="QR length 1"),
            pytest.param("12", ConnectionError, id="QR length 2"),
            pytest.param("1234", ConnectionError, id="QR length 4"),
            pytest.param("123456", ConnectionError, id="QR length 6"),
            pytest.param("12345678", ConnectionError, id="QR length 8"),
        ],
    )
    def test_not_db_check_len_color(self, qr, exepted_error):
        checker = CheckQr()
        with pytest.raises(exepted_error):
            assert checker.check_scanned_device(qr)

    @pytest.mark.parametrize(
        "qr",
        [
            pytest.param("1", id="QR length 1"),
            pytest.param("12", id="QR length 2"),
            pytest.param("1234", id="QR length 4"),
            pytest.param("123456", id="QR length 6"),
            pytest.param("12345678", id="QR length 8"),
        ],
    )
    @patch.object(CheckQr, "send_error")
    @patch.object(CheckQr, "check_in_db", return_value=True)
    def test_wrong_qr_length(self, mock_db, mock_send_error, qr):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        mock_send_error.assert_called_once_with(
            f"Error: Wrong qr length {len(qr)}"
        )

    @pytest.mark.parametrize(
        "qr",
        [
            pytest.param("123", id="QR length 3"),
            pytest.param("12345", id="QR length 5"),
            pytest.param("1234567", id="QR length 7"),
        ],
    )
    @patch.object(CheckQr, "check_in_db", return_value=None)
    @patch.object(CheckQr, "send_error")
    def test_qr_not_in_db(self, mock_send_error, mock_db, qr):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        mock_send_error.assert_called_once_with("Not in DB")

    @pytest.mark.parametrize(
        "qr",
        [
            pytest.param("123", id="QR length 3"),
            pytest.param("12345", id="QR length 5"),
            pytest.param("1234567", id="QR length 7"),
        ],
    )
    @patch.object(CheckQr, "can_add_device")
    @patch.object(CheckQr, "check_in_db", return_value=True)
    def test_can_add_device_called_once(
        self, mock_db, mock_can_add_device, qr
    ):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        mock_can_add_device.assert_called_once_with(f"hallelujah {qr}")

    @pytest.mark.parametrize(
        "qr",
        [
            pytest.param("123", id="QR length 3"),
            pytest.param("12345", id="QR length 5"),
            pytest.param("1234567", id="QR length 7"),
        ],
    )
    @patch.object(CheckQr, "can_add_device")
    @patch.object(CheckQr, "check_in_db", return_value=None)
    def test_can_add_device_not_called_once(
        self, mock_db, mock_can_add_device, qr
    ):
        checker = CheckQr()
        checker.check_scanned_device(qr)
        mock_can_add_device.assert_not_called()
