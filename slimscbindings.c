/*
  Python C extensions for Slim's Editor.
  Checksum method copied from https://github.com/stiantoften/RC-checksum/
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>


// Read a little endian unsigned int from a byte buffer
uint32_t readInt(const uint8_t *buffer, const uint32_t seek) {
    return ((buffer[seek + 3u] & 0xFFu) << 24u
            | (buffer[seek + 2u] & 0xFFu) << 16u
            | (buffer[seek + 1u] & 0xFFu) << 8u
            | (buffer[seek] & 0xFFu));
}

// Write a little endian unsigned int to a byte buffer
void writeInt(uint8_t *buffer, const uint32_t seek, const uint32_t value) {
    buffer[seek] = value;
    buffer[seek+1] = value >> 8;
    buffer[seek+2] = value >> 16;
    buffer[seek+3] = value >> 24;
}

static PyObject * slimscbindings_calculate_checksum(PyObject *self, PyObject *args)
{
    PyByteArrayObject* data = NULL;
    if (!PyArg_ParseTuple(args, "Y", &data)) {
        return Py_None;
    }

    long filesize = PyByteArray_Size(data);
    char* buffer = PyByteArray_AsString(data);

    uint32_t pos = 0x08;
    while (pos < filesize) {
        uint32_t bytecount = readInt(buffer, pos);
        uint32_t prevchecksum = readInt(buffer, pos + 4);
        pos += 0x08;
        uint32_t prevpos = pos;

        // Exit if the section length seems incorrect
        if (bytecount <= 0x20 || bytecount > 0xFFFF) {
            return Py_None;
        }

        // Calculate checksum of the section
        uint32_t checksum = 0x8320;
        while (pos < prevpos + bytecount) {
            checksum ^= ((buffer[pos++] & 0xFFu) << 8u);
            for (int i = 0; i < 8; i++) {
                checksum = checksum & 0x8000u ? (checksum << 1u) ^ 0x1F45u : checksum << 1u;
            }
        }

        // The calculated checksum is 4 bytes, but the save only uses the lower 2
        checksum &= 0xFFFFu;

        // Write the new checksum
        if (checksum != prevchecksum) {
            writeInt(buffer, prevpos - 4, checksum);
        }
    }

    return PyByteArray_FromStringAndSize(buffer, filesize);
}

static PyMethodDef SlimsCBindingsMethods[] = {
    {"calculate_checksum",
     slimscbindings_calculate_checksum,
     METH_VARARGS,
     "Calculate checksum for OG trilogy games."},

    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef slimscbindings = {
    PyModuleDef_HEAD_INIT,
    "slimscbindings",
    NULL,
    -1,
    SlimsCBindingsMethods
};

PyMODINIT_FUNC PyInit_slimscbindings(void) {
    return PyModule_Create(&slimscbindings);
}

