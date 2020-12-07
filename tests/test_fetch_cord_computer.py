import unittest

from fetch_cord.computer.Computer import Computer


def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare


ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare


class TestFetchCordComputer(unittest.TestCase):
    """Test class for Computer module"""

    pc: Computer

    @classmethod
    def setUpClass(cls):
        """Setup the Computer class and load the neofetch info"""

        cls.pc = Computer()

    @classmethod
    def tearDownClass(self):
        """Called once at the end"""
        pass

    @ordered
    def test_detected_os(self):
        """Test the detected os result"""

        print("Detected OS : " + self.pc.os)

    @ordered
    def test_detected_neofetch(self):
        """Test detected neofetch"""

        print("Detected Neofetch : ", end="")
        if self.pc.neofetch:
            print("neofetch")
        elif self.pc.neofetchwin:
            print("neofetch-win")
        else:
            print("None")

    @ordered
    def test_detected_cpu(self):
        """Test detected CPU"""

        if len(self.pc.cpu) == 0 or self.pc.cpu == ["N/A"]:
            print("No CPU detected !")
        else:
            for cpu in self.pc.cpu:
                print("Detected CPU : " + cpu.model)
                print("Detected CPU Temp : " + str(cpu.temp) + "°c")

    @ordered
    def test_detected_gpu(self):
        """Test detected GPU"""

        if len(self.pc.gpu) == 0 or self.pc.gpu == ["N/A"]:
            print("No GPU detected !")
        else:
            for gpu in self.pc.gpu:
                print("Detected GPU : " + gpu.model)

    @ordered
    def test_detected_disks(self):
        """Test detected disks"""

        if len(self.pc.disks) == 0 or self.pc.disks == ["N/A"]:
            print("No Disk detected !")
        else:
            for disk in self.pc.disks:
                print("Detected Disk : " + disk)

    @ordered
    def test_detected_memory(self):
        """Test detected memory"""

        print("Detected Memory : " + "\t".join(self.pc.memory))

    @ordered
    def test_detected_osinfo(self):
        """Test detected OS info"""

        print("Detected OS info : " + "\t".join(self.pc.osinfo))

    @ordered
    def test_detected_motherboard(self):
        """Test detected motherboard"""

        print("Detected Motherboard : " + "\t".join(self.pc.motherboard))

    @ordered
    def test_detected_host(self):
        """Test detected host"""

        print("Detected host : " + "\t".join(self.pc.host))

    @ordered
    def test_detected_resolution(self):
        """Test detected resolution"""

        print("Detected resolution : " + "\t".join(self.pc.resolution))

    @ordered
    def test_detected_theme(self):
        """Test detected theme"""

        print("Detected theme : " + "\t".join(self.pc.theme))

    @ordered
    def test_detected_packages(self):
        """Test detected packages"""

        print("Detected packages : " + "\t".join(self.pc.packages))

    @ordered
    def test_detected_shell(self):
        """Test detected shell"""

        print("Detected shell : " + "\t".join(self.pc.shell))

    @ordered
    def test_detected_kernel(self):
        """Test detected kernel"""

        print("Detected kernel : " + "\t".join(self.pc.kernel))

    @ordered
    def test_detected_terminal(self):
        """Test detected terminal"""

        print("Detected terminal : " + "\t".join(self.pc.terminal))

    @ordered
    def test_detected_font(self):
        """Test detected font"""

        print("Detected font : " + "\t".join(self.pc.font))

    @ordered
    def test_detected_de(self):
        """Test detected de"""

        print("Detected de : " + "\t".join(self.pc.de))

    @ordered
    def test_detected_wm(self):
        """Test detected wm"""

        print("Detected wm : " + "\t".join(self.pc.wm))


if __name__ == "__main__":
    unittest.main()
