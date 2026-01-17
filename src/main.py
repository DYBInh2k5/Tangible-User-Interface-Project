#!/usr/bin/env python3
"""
Tangible User Interface - Main Application
Ứng dụng chính cho hệ thống bàn tương tác
"""

import pygame
import cv2
import sys
from camera.camera_manager import CameraManager
from detection.object_detector import ObjectDetector
from visualization.ui_renderer import UIRenderer

class TangibleUI:
    def __init__(self):
        """Khởi tạo hệ thống TUI"""
        pygame.init()
        
        # Cấu hình màn hình
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tangible User Interface - TAN25.11")
        
        # Khởi tạo các thành phần
        self.camera_manager = CameraManager()
        self.object_detector = ObjectDetector()
        self.ui_renderer = UIRenderer(self.screen)
        
        self.running = True
        self.clock = pygame.time.Clock()
        
    def run(self):
        """Vòng lặp chính của ứng dụng"""
        print("Khởi động Tangible User Interface...")
        
        while self.running:
            # Xử lý events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Capture frame từ camera
            frame = self.camera_manager.get_frame()
            if frame is not None:
                # Detect objects
                detected_objects = self.object_detector.detect(frame)
                
                # Render UI
                self.ui_renderer.render(detected_objects)
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        self.cleanup()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.camera_manager.release()
        pygame.quit()
        print("Đã thoát ứng dụng")

if __name__ == "__main__":
    try:
        app = TangibleUI()
        app.run()
    except KeyboardInterrupt:
        print("\nThoát ứng dụng...")
        sys.exit(0)
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)