"""
Camera Manager - Quản lý camera và xử lý hình ảnh
"""

import cv2
import numpy as np

class CameraManager:
    def __init__(self, camera_id=0):
        """
        Khởi tạo camera manager
        Args:
            camera_id: ID của camera (mặc định 0)
        """
        self.camera_id = camera_id
        self.cap = None
        self.frame_width = 1280
        self.frame_height = 720
        
        self.initialize_camera()
        
    def initialize_camera(self):
        """Khởi tạo và cấu hình camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                raise Exception(f"Không thể mở camera {self.camera_id}")
            
            # Cấu hình camera
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"Camera {self.camera_id} đã được khởi tạo thành công")
            
        except Exception as e:
            print(f"Lỗi khởi tạo camera: {e}")
            self.cap = None
    
    def get_frame(self):
        """
        Lấy frame từ camera
        Returns:
            numpy.ndarray: Frame hình ảnh hoặc None nếu lỗi
        """
        if self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Flip frame để tạo hiệu ứng mirror
        frame = cv2.flip(frame, 1)
        
        # Áp dụng các bộ lọc tiền xử lý
        frame = self.preprocess_frame(frame)
        
        return frame
    
    def preprocess_frame(self, frame):
        """
        Tiền xử lý frame để tối ưu cho object detection
        Args:
            frame: Frame gốc
        Returns:
            numpy.ndarray: Frame đã được xử lý
        """
        # Giảm noise
        frame = cv2.bilateralFilter(frame, 9, 75, 75)
        
        # Tăng độ tương phản
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
        
        return frame
    
    def get_camera_info(self):
        """Lấy thông tin camera"""
        if self.cap is None:
            return None
            
        info = {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.cap.get(cv2.CAP_PROP_FPS))
        }
        return info
    
    def release(self):
        """Giải phóng camera"""
        if self.cap is not None:
            self.cap.release()
            print("Camera đã được giải phóng")