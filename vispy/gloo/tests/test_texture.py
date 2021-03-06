# -----------------------------------------------------------------------------
# VisPy - Copyright (c) 2013, Vispy Development Team
# All rights reserved.
# -----------------------------------------------------------------------------
import unittest
import numpy as np
from vispy.gloo import gl
from vispy.gloo.texture import Texture, Texture2D, Texture3D



class TextureBasetests:
    
    def test_init(self):
        
        data = np.zeros(self._shape0, np.float32)
        tex = self._klass(data)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE)
        self.assertEqual(tex._levels[0].shape, data.shape)
    
    
    def test_allocating_data(self):
        
        tex = self._klass()
        
        # Luminance
        tex.set_shape(self._shape0)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE)
        self.assertEqual(tex._levels[0].shape, self._shape0)
        
        # Luminance again, but now an explicit color channel
        tex.set_shape(self._shape1)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE)
        self.assertEqual(tex._levels[0].shape, self._shape1)
        
        # Luminance + alpha
        tex.set_shape(self._shape2)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE_ALPHA)
        self.assertEqual(tex._levels[0].shape, self._shape2)
        
        # RGB
        tex.set_shape(self._shape3)
        self.assertEqual(tex._levels[0].format, gl.GL_RGB)
        self.assertEqual(tex._levels[0].shape, self._shape3)
        
        # RGBA
        tex.set_shape(self._shape4)
        self.assertEqual(tex._levels[0].format, gl.GL_RGBA)
        self.assertEqual(tex._levels[0].shape, self._shape4)
        
        # Alpha
        tex.set_shape(self._shape0, format=gl.GL_ALPHA)
        self.assertEqual(tex._levels[0].format, gl.GL_ALPHA)
        self.assertEqual(tex._levels[0].shape, self._shape0)
    
    
    def test_setting_data(self):
        
        tex = self._klass()
        
        # Luminance
        data = np.zeros(self._shape0, np.float32)
        tex.set_data(data)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE)
        self.assertEqual(tex._levels[0].shape, data.shape)
        
        # Luminance again, but now an explicit color channel
        data = np.zeros(self._shape1, np.float32)
        tex.set_data(data)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE)
        self.assertEqual(tex._levels[0].shape, data.shape)
        
        # Luminance + alpha
        data = np.zeros(self._shape2, np.float32)
        tex.set_data(data)
        self.assertEqual(tex._levels[0].format, gl.GL_LUMINANCE_ALPHA)
        self.assertEqual(tex._levels[0].shape, data.shape)
        
        # RGB
        data = np.zeros(self._shape3, np.float32)
        tex.set_data(data)
        self.assertEqual(tex._levels[0].format, gl.GL_RGB)
        self.assertEqual(tex._levels[0].shape, data.shape)
        
        # RGBA
        data = np.zeros(self._shape4, np.float32)
        tex.set_data(data)
        self.assertEqual(tex._levels[0].format, gl.GL_RGBA)
        self.assertEqual(tex._levels[0].shape, data.shape)
        
        # Alpha
        data = np.zeros(self._shape0, np.float32)
        tex.set_data(data, format=gl.GL_ALPHA)
        self.assertEqual(tex._levels[0].format, gl.GL_ALPHA)
        self.assertEqual(tex._levels[0].shape, data.shape)
    
    
    def test_invalid_shape(self):
        
        tex = self._klass()
        
        data = np.zeros(self._shape5, np.float32)
        with self.assertRaises(ValueError):
            tex.set_data(data)
        
        # Format and shape mismatch
        data = np.zeros(self._shape1, np.float32)
        with self.assertRaises(ValueError):
            tex.set_data(data, format=gl.GL_RGB)
        
        # Format and shape mismatch
        data = np.zeros(self._shape3, np.float32)
        with self.assertRaises(ValueError):
            tex.set_data(data, format=gl.GL_RGBA)
        
        # Format and shape mismatch
        data = np.zeros(self._shape4, np.float32)
        with self.assertRaises(ValueError):
            tex.set_data(data, format=gl.GL_RGB)
        
        # Format and shape mismatch
        data = np.zeros(self._shape3, np.float32)
        with self.assertRaises(ValueError):
            tex.set_data(data, format=gl.GL_ALPHA)
    
    def test_dtype(self):
        pass  # No use, we convert dtype if necessary
    
    
    def test_subdata(self):
        
        tex = self._klass()
        data = np.zeros(self._shape0, np.float32)
        offset1 = [0 for i in self._shape0]
        offset2 = [10 for i in self._shape0]
        
        # No pending data now
        self.assertEqual(len(tex._levels), 0)
        
        # No data allocated yet
        with self.assertRaises(RuntimeError):
            tex.set_subdata(offset1, data)
        
        # Allocate data
        tex.set_shape(data.shape)
        
        # Pending data
        self.assertEqual(tex._levels[0].need_resize, True)
        self.assertEqual(len(tex._levels[0].pending_data), 0)
        
        # Now it should work
        tex.set_subdata(offset1, data)
        self.assertEqual(len(tex._levels[0].pending_data), 1)
        #
        tex.set_subdata(offset1, data)
        self.assertEqual(len(tex._levels[0].pending_data), 2)
        
        # Reset using set_shape  (no pending data)
        tex.set_shape(data.shape)
        self.assertEqual(len(tex._levels[0].pending_data), 0)
        
        # Again
        tex.set_subdata(offset1, data)
        tex.set_subdata(offset1, data)
        self.assertEqual(len(tex._levels[0].pending_data), 2)
        
        # Reset using set_data (1 pending data)
        tex.set_data(data)
        self.assertEqual(len(tex._levels[0].pending_data), 1)

    
    def test_subdata_shape_and_format(self):
        
        tex = self._klass()
        data = np.zeros(self._shape0, np.float32)
        offset1 = [0 for i in self._shape0]
        offset2 = [9 for i in self._shape0]
        offset3 = [-1 for i in self._shape0]
        offset4 = [11 for i in self._shape0]
        
        # Allocate data
        tex.set_shape([i+10 for i in self._shape0])
        
        # Some stuff that should work
        tex.set_subdata(offset1, data)
        tex.set_subdata(offset2, data)
        
        # Some stuff that should not (shape)
        with self.assertRaises(ValueError):
            tex.set_subdata(offset3, data)
        with self.assertRaises(ValueError):
            tex.set_subdata(offset4, data)
        
        # More stuff that should not (format)
        with self.assertRaises(ValueError):
            tex.set_subdata(offset1, data, format=gl.GL_RGB)
        with self.assertRaises(ValueError):
            tex.set_subdata(offset1, data, format=gl.GL_LUMINANCE_ALPHA)
        with self.assertRaises(ValueError):
            tex.set_subdata(offset1, data,format= gl.GL_LUMINANCE_ALPHA)
        
        # But this should work
        tex.set_shape([i+10 for i in self._shape0], format=gl.GL_ALPHA)
        tex.set_subdata(offset1, data)
    
    
    def test_levels(self):
        
        # Create tex
        tex = self._klass()
        self.assertEqual(len(tex._levels), 0)
        
        # Create level 0
        tex.set_shape(self._shape3)
        self.assertEqual(len(tex._levels), 1)
        self.assertIn(0, tex._levels)
        
        # Create level 2
        tex.set_shape(self._shape3, 2)
        self.assertEqual(len(tex._levels), 2)
        self.assertIn(0, tex._levels)
        self.assertIn(2, tex._levels)
        
        # Create level 4
        tex.set_shape(self._shape3, 4)
        self.assertEqual(len(tex._levels), 3)
        self.assertIn(0, tex._levels)
        self.assertIn(2, tex._levels)
        self.assertIn(4, tex._levels)
    


class Texture2DTest(TextureBasetests, unittest.TestCase):
    def setUp(self):
        self._klass = Texture2D
        self._shape0 = 100, 100
        self._shape1 = 100, 100, 1
        self._shape2 = 100, 100, 2
        self._shape3 = 100, 100, 3
        self._shape4 = 100, 100, 4
        self._shape5 = 100, 100, 5



class Texture3DTest(TextureBasetests, unittest.TestCase):
    def setUp(self):
        self._klass = Texture3D
        self._shape0 = 10, 10, 10
        self._shape1 = 10, 10, 10, 1
        self._shape2 = 10, 10, 10, 2
        self._shape3 = 10, 10, 10, 3
        self._shape4 = 10, 10, 10, 4
        self._shape5 = 10, 10, 10, 5


if __name__ == "__main__":
    unittest.main()
#     t = Texture2DTest()
#     t.setUp()
#     t.test_invalid_shape()
