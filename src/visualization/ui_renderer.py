"""
UI Renderer - Hiển thị giao diện tương tác
"""

import pygame
import math
import numpy as np
from typing import List
from detection.object_detector import TangibleObject

class UIRenderer:
    def __init__(self, screen):
        """
        Khởi tạo UI renderer
        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Màu sắc
        self.colors = {
            'background': (20, 30, 50),
            'table_surface': (0, 100, 200),
            'connection_line': (255, 255, 255),
            'object_glow': (100, 200, 255),
            'green_cube': (0, 255, 0),
            'red_cube': (255, 0, 0),
            'blue_cube': (0, 0, 255),
            'text': (255, 255, 255)
        }
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Tâm bàn tròn
        self.table_center = (self.width // 2, self.height // 2)
        self.table_radius = min(self.width, self.height) // 3
        
        # Animation
        self.animation_time = 0
        
    def render(self, objects: List[TangibleObject]):
        """
        Render giao diện chính
        Args:
            objects: Danh sách objects để hiển thị
        """
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Vẽ bàn tương tác
        self.draw_interactive_table()
        
        # Vẽ objects và effects
        self.draw_objects(objects)
        
        # Vẽ connections giữa objects
        self.draw_connections(objects)
        
        # Vẽ UI info
        self.draw_ui_info(objects)
        
        # Update animation
        self.animation_time += 1
    
    def draw_interactive_table(self):
        """Vẽ bề mặt bàn tương tác"""
        # Vẽ bàn tròn chính
        pygame.draw.circle(
            self.screen, 
            self.colors['table_surface'], 
            self.table_center, 
            self.table_radius, 
            0
        )
        
        # Vẽ viền bàn
        pygame.draw.circle(
            self.screen, 
            self.colors['connection_line'], 
            self.table_center, 
            self.table_radius, 
            3
        )
        
        # Vẽ các vòng tròn đồng tâm (hiệu ứng)
        for i in range(3):
            alpha = 50 + 30 * math.sin(self.animation_time * 0.05 + i)
            radius = self.table_radius - 50 - i * 30
            
            if radius > 0:
                # Tạo surface với alpha
                circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    circle_surface, 
                    (*self.colors['object_glow'], int(alpha)), 
                    (radius, radius), 
                    radius, 
                    2
                )
                
                self.screen.blit(
                    circle_surface, 
                    (self.table_center[0] - radius, self.table_center[1] - radius)
                )
    
    def draw_objects(self, objects: List[TangibleObject]):
        """
        Vẽ các tangible objects
        Args:
            objects: Danh sách objects
        """
        for obj in objects:
            self.draw_single_object(obj)
    
    def draw_single_object(self, obj: TangibleObject):
        """
        Vẽ một object đơn lẻ
        Args:
            obj: TangibleObject để vẽ
        """
        x, y = obj.position
        
        # Chọn màu theo loại object
        color = self.colors.get(obj.object_type, self.colors['object_glow'])
        
        # Vẽ vòng tròn glow xung quanh object
        glow_radius = 40 + 10 * math.sin(self.animation_time * 0.1)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surface, 
            (*color, 100), 
            (glow_radius, glow_radius), 
            glow_radius
        )
        self.screen.blit(glow_surface, (x - glow_radius, y - glow_radius))
        
        # Vẽ object chính
        pygame.draw.circle(self.screen, color, (x, y), 20, 0)
        pygame.draw.circle(self.screen, self.colors['connection_line'], (x, y), 20, 2)
        
        # Vẽ indicator cho rotation
        end_x = x + 15 * math.cos(math.radians(obj.rotation))
        end_y = y + 15 * math.sin(math.radians(obj.rotation))
        pygame.draw.line(self.screen, self.colors['connection_line'], (x, y), (end_x, end_y), 3)
        
        # Vẽ ID object
        id_text = self.small_font.render(str(obj.id), True, self.colors['text'])
        text_rect = id_text.get_rect(center=(x, y - 35))
        self.screen.blit(id_text, text_rect)
    
    def draw_connections(self, objects: List[TangibleObject]):
        """
        Vẽ các đường kết nối giữa objects
        Args:
            objects: Danh sách objects
        """
        if len(objects) < 2:
            return
        
        # Vẽ kết nối giữa tất cả các objects
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects[i+1:], i+1):
                self.draw_connection_line(obj1, obj2)
    
    def draw_connection_line(self, obj1: TangibleObject, obj2: TangibleObject):
        """
        Vẽ đường kết nối giữa 2 objects
        Args:
            obj1, obj2: Hai objects để kết nối
        """
        x1, y1 = obj1.position
        x2, y2 = obj2.position
        
        # Tính khoảng cách
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Chỉ vẽ nếu khoảng cách hợp lý
        if distance < 300:
            # Hiệu ứng animated line
            alpha = 100 + 50 * math.sin(self.animation_time * 0.08)
            
            # Tạo surface cho line với alpha
            line_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.line(
                line_surface, 
                (*self.colors['connection_line'], int(alpha)), 
                (x1, y1), 
                (x2, y2), 
                2
            )
            self.screen.blit(line_surface, (0, 0))
            
            # Vẽ điểm giữa đường kết nối
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            pygame.draw.circle(self.screen, self.colors['object_glow'], (mid_x, mid_y), 5)
    
    def draw_ui_info(self, objects: List[TangibleObject]):
        """
        Vẽ thông tin UI
        Args:
            objects: Danh sách objects
        """
        # Tiêu đề
        title = self.font.render("Tangible User Interface - TAN25.11", True, self.colors['text'])
        self.screen.blit(title, (20, 20))
        
        # Thông tin objects
        info_y = 70
        info_text = f"Objects detected: {len(objects)}"
        info_surface = self.small_font.render(info_text, True, self.colors['text'])
        self.screen.blit(info_surface, (20, info_y))
        
        # Danh sách objects
        for i, obj in enumerate(objects[:5]):  # Hiển thị tối đa 5 objects
            obj_info = f"ID {obj.id}: {obj.object_type} at ({obj.position[0]}, {obj.position[1]})"
            obj_surface = self.small_font.render(obj_info, True, self.colors['text'])
            self.screen.blit(obj_surface, (20, info_y + 30 + i * 25))
        
        # Instructions
        instructions = [
            "ESC: Thoát ứng dụng",
            "Đặt các khối màu lên bàn để tương tác"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, self.colors['text'])
            self.screen.blit(inst_surface, (20, self.height - 60 + i * 25))