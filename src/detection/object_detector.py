"""
Object Detector - Nhận diện và theo dõi các đối tượng tangible
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple

class TangibleObject:
    def __init__(self, id: int, position: Tuple[int, int], rotation: float, object_type: str):
        self.id = id
        self.position = position  # (x, y)
        self.rotation = rotation  # góc xoay (degrees)
        self.object_type = object_type
        self.last_seen = 0
        self.confidence = 0.0

class ObjectDetector:
    def __init__(self):
        """Khởi tạo object detector"""
        self.objects = {}  # Dictionary lưu trữ các object được track
        self.next_id = 0
        
        # Tham số cho contour detection
        self.min_contour_area = 500
        self.max_contour_area = 5000
        
        # Tham số cho color detection
        self.setup_color_ranges()
        
    def setup_color_ranges(self):
        """Thiết lập các dải màu để nhận diện objects"""
        # HSV color ranges cho các loại object khác nhau
        self.color_ranges = {
            'green_cube': {
                'lower': np.array([40, 50, 50]),
                'upper': np.array([80, 255, 255])
            },
            'red_cube': {
                'lower': np.array([0, 50, 50]),
                'upper': np.array([10, 255, 255])
            },
            'blue_cube': {
                'lower': np.array([100, 50, 50]),
                'upper': np.array([130, 255, 255])
            }
        }
    
    def detect(self, frame) -> List[TangibleObject]:
        """
        Nhận diện objects trong frame
        Args:
            frame: Frame hình ảnh từ camera
        Returns:
            List[TangibleObject]: Danh sách objects được phát hiện
        """
        if frame is None:
            return []
        
        # Chuyển đổi sang HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        detected_objects = []
        
        # Detect từng loại object theo màu
        for object_type, color_range in self.color_ranges.items():
            objects = self.detect_by_color(hsv, object_type, color_range)
            detected_objects.extend(objects)
        
        # Update tracking
        self.update_tracking(detected_objects)
        
        return list(self.objects.values())
    
    def detect_by_color(self, hsv_frame, object_type: str, color_range: Dict) -> List[TangibleObject]:
        """
        Nhận diện objects theo màu sắc
        Args:
            hsv_frame: Frame HSV
            object_type: Loại object
            color_range: Dải màu HSV
        Returns:
            List[TangibleObject]: Objects được phát hiện
        """
        # Tạo mask cho màu
        mask = cv2.inRange(hsv_frame, color_range['lower'], color_range['upper'])
        
        # Morphological operations để làm sạch mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Tìm contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Lọc theo diện tích
            if self.min_contour_area < area < self.max_contour_area:
                # Tính toán vị trí và góc xoay
                moments = cv2.moments(contour)
                if moments['m00'] != 0:
                    cx = int(moments['m10'] / moments['m00'])
                    cy = int(moments['m01'] / moments['m00'])
                    
                    # Tính góc xoay từ contour
                    rotation = self.calculate_rotation(contour)
                    
                    # Tạo object mới
                    obj = TangibleObject(
                        id=self.next_id,
                        position=(cx, cy),
                        rotation=rotation,
                        object_type=object_type
                    )
                    obj.confidence = min(area / self.max_contour_area, 1.0)
                    
                    objects.append(obj)
                    self.next_id += 1
        
        return objects
    
    def calculate_rotation(self, contour) -> float:
        """
        Tính toán góc xoay của object từ contour
        Args:
            contour: Contour của object
        Returns:
            float: Góc xoay (degrees)
        """
        try:
            # Fit ellipse để tính góc
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                angle = ellipse[2]
                return angle
            else:
                return 0.0
        except:
            return 0.0
    
    def update_tracking(self, new_objects: List[TangibleObject]):
        """
        Cập nhật tracking cho các objects
        Args:
            new_objects: Danh sách objects mới phát hiện
        """
        # Đơn giản hóa: chỉ cập nhật objects hiện tại
        # Trong thực tế cần thuật toán tracking phức tạp hơn
        self.objects.clear()
        
        for obj in new_objects:
            self.objects[obj.id] = obj
    
    def get_object_by_position(self, x: int, y: int, threshold: int = 50) -> TangibleObject:
        """
        Tìm object gần nhất với vị trí cho trước
        Args:
            x, y: Tọa độ
            threshold: Ngưỡng khoảng cách
        Returns:
            TangibleObject hoặc None
        """
        min_distance = float('inf')
        closest_object = None
        
        for obj in self.objects.values():
            distance = np.sqrt((obj.position[0] - x)**2 + (obj.position[1] - y)**2)
            if distance < min_distance and distance < threshold:
                min_distance = distance
                closest_object = obj
        
        return closest_object