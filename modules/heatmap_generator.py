# modules/heatmap_generator.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

class HeatmapGenerator:
    """Generates heatmaps with football pitch background"""
    
    def __init__(self):
        # Standard football pitch dimensions (meters)
        self.pitch_length = 105.0
        self.pitch_width = 68.0
        
        # Define colors
        self.pitch_color = '#3CB371'  # Green
        self.line_color = 'white'
        self.background_color = '#2E8B57'  # Dark green
        
        # Custom heatmap colormap
        colors = ['#000033', '#87CEEB', '#00FF00', '#FFFF00', '#FFA500', '#FF0000', '#8B0000']

        #colors = ['#000033', '#000080', '#0000FF', '#00FFFF', '#FFFF00', '#FF0000', '#FFFFFF']
        self.cmap = LinearSegmentedColormap.from_list('custom_heat', colors, N=100)
    
    def generate_heatmap(self, positions, player_id=None, position_name="Unknown", bins=60):
        """
        Generate heatmap with football pitch background
        
        Args:
            positions: numpy array of shape (n, 2) with [x, y] positions in meters
            player_id: Player ID number
            position_name: Player position name
            bins: Number of bins for histogram
            
        Returns:
            matplotlib figure object
        """
        if positions is None or len(positions) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Draw football pitch background
        self._draw_pitch_background(ax)
        
        # Extract x and y coordinates
        x = positions[:, 0]
        y = positions[:, 1]
        
        # Clip to pitch boundaries
        x = np.clip(x, 0, self.pitch_length)
        y = np.clip(y, 0, self.pitch_width)
        
        # Create heatmap
        heatmap, xedges, yedges = np.histogram2d(
            x, y,
            bins=bins,
            range=[[0, self.pitch_length], [0, self.pitch_width]]
        )
        
        # Apply Gaussian filter for smoothing
        try:
            heatmap = gaussian_filter(heatmap, sigma=2)
        except:
            pass  # Continue without smoothing if scipy not available
        
        # Plot heatmap with transparency
        extent = [0, self.pitch_length, 0, self.pitch_width]
        im = ax.imshow(
            heatmap.T, extent=extent, origin='lower',
            cmap=self.cmap, aspect='auto', alpha=0.7,
            interpolation='bilinear'
        )
        
        # Set title
        if player_id is not None:
            title = f"Player #{player_id} - {position_name} Movement Heatmap"
        else:
            title = "Movement Heatmap"
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Field Length (meters)')
        ax.set_ylabel('Field Width (meters)')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='Activity Density', fraction=0.046, pad=0.04)
        
        # Set pitch limits and invert y-axis
        ax.set_xlim(0, self.pitch_length)
        ax.set_ylim(0, self.pitch_width)
        ax.invert_yaxis()  # Match typical football view
        
        plt.tight_layout()
        return fig
    
    def _draw_pitch_background(self, ax):
        """Draw a football pitch background"""
        
        # Pitch outline (green)
        pitch_rect = Rectangle((0, 0), self.pitch_length, self.pitch_width, 
                              linewidth=2, edgecolor=self.line_color, 
                              facecolor=self.pitch_color, alpha=0.7)
        ax.add_patch(pitch_rect)
        
        # Halfway line
        ax.axvline(x=self.pitch_length/2, color=self.line_color, linewidth=2, linestyle='-')
        
        # Center circle
        center_circle = Circle((self.pitch_length/2, self.pitch_width/2), 9.15, 
                              color=self.line_color, fill=False, linewidth=2)
        ax.add_patch(center_circle)
        
        # Center spot
        ax.plot(self.pitch_length/2, self.pitch_width/2, 'wo', markersize=6)
        
        # Penalty areas
        penalty_length = 16.5
        penalty_width = 40.3
        penalty_y = (self.pitch_width - penalty_width) / 2
        
        # Left penalty area (defensive)
        left_penalty = Rectangle((0, penalty_y), penalty_length, penalty_width,
                                linewidth=2, edgecolor=self.line_color, facecolor='none')
        ax.add_patch(left_penalty)
        
        # Right penalty area (attacking)
        right_penalty = Rectangle((self.pitch_length - penalty_length, penalty_y), 
                                 penalty_length, penalty_width,
                                 linewidth=2, edgecolor=self.line_color, facecolor='none')
        ax.add_patch(right_penalty)
        
        # Goal areas
        goal_length = 5.5
        goal_width = 18.3
        goal_y = (self.pitch_width - goal_width) / 2
        
        # Left goal area
        left_goal = Rectangle((0, goal_y), goal_length, goal_width,
                             linewidth=2, edgecolor=self.line_color, facecolor='none')
        ax.add_patch(left_goal)
        
        # Right goal area
        right_goal = Rectangle((self.pitch_length - goal_length, goal_y), 
                              goal_length, goal_width,
                              linewidth=2, edgecolor=self.line_color, facecolor='none')
        ax.add_patch(right_goal)
        
        # Penalty spots
        ax.plot(11, self.pitch_width/2, 'wo', markersize=4)  # Left penalty spot
        ax.plot(self.pitch_length - 11, self.pitch_width/2, 'wo', markersize=4)  # Right penalty spot
        
        # Corner arcs (quarter circles)
        corner_radius = 1
        
        # Top-left corner
        arc_tl = Arc((0, self.pitch_width), width=corner_radius*2, height=corner_radius*2,
                    angle=0, theta1=270, theta2=360, color=self.line_color, linewidth=2)
        # Top-right corner
        arc_tr = Arc((self.pitch_length, self.pitch_width), width=corner_radius*2, height=corner_radius*2,
                    angle=0, theta1=180, theta2=270, color=self.line_color, linewidth=2)
        # Bottom-left corner
        arc_bl = Arc((0, 0), width=corner_radius*2, height=corner_radius*2,
                    angle=0, theta1=0, theta2=90, color=self.line_color, linewidth=2)
        # Bottom-right corner
        arc_br = Arc((self.pitch_length, 0), width=corner_radius*2, height=corner_radius*2,
                    angle=0, theta1=90, theta2=180, color=self.line_color, linewidth=2)
        
        ax.add_patch(arc_tl)
        ax.add_patch(arc_tr)
        ax.add_patch(arc_bl)
        ax.add_patch(arc_br)
        
        # Add direction arrows
        ax.annotate('← Defensive', xy=(10, self.pitch_width + 2), xycoords='data',
                   fontsize=10, color='white', fontweight='bold')
        ax.annotate('Attacking →', xy=(self.pitch_length - 40, self.pitch_width + 2), xycoords='data',
                   fontsize=10, color='white', fontweight='bold')
        
        # Set background to dark green
        ax.set_facecolor(self.background_color)
        
        # Set aspect ratio
        ax.set_aspect('equal')
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
    
    def generate_comparison_heatmap(self, positions_list, player_ids=None, position_names=None):
        """
        Generate comparison heatmap for multiple players
        
        Args:
            positions_list: List of numpy arrays, each with shape (n, 2)
            player_ids: List of player IDs
            position_names: List of position names
            
        Returns:
            matplotlib figure object
        """
        if not positions_list:
            return None
        
        n_players = len(positions_list)
        fig, axes = plt.subplots(1, n_players, figsize=(6*n_players, 8))
        
        if n_players == 1:
            axes = [axes]
        
        for i, (positions, ax) in enumerate(zip(positions_list, axes)):
            if player_ids and i < len(player_ids):
                player_id = player_ids[i]
            else:
                player_id = None
            
            if position_names and i < len(position_names):
                position_name = position_names[i]
            else:
                position_name = f"Player {i+1}"
            
            # Draw pitch background
            self._draw_pitch_background(ax)
            
            if positions is not None and len(positions) > 0:
                # Extract and clip coordinates
                x = np.clip(positions[:, 0], 0, self.pitch_length)
                y = np.clip(positions[:, 1], 0, self.pitch_width)
                
                # Create heatmap
                heatmap, _, _ = np.histogram2d(
                    x, y,
                    bins=40,
                    range=[[0, self.pitch_length], [0, self.pitch_width]]
                )
                
                try:
                    heatmap = gaussian_filter(heatmap, sigma=2)
                except:
                    pass
                
                # Plot heatmap
                extent = [0, self.pitch_length, 0, self.pitch_width]
                im = ax.imshow(
                    heatmap.T, extent=extent, origin='lower',
                    cmap=self.cmap, aspect='auto', alpha=0.7,
                    interpolation='bilinear'
                )
            
            ax.set_title(f"{position_name}", fontsize=12, fontweight='bold')
            ax.set_xlim(0, self.pitch_length)
            ax.set_ylim(0, self.pitch_width)
            ax.invert_yaxis()
        
        plt.tight_layout()
        return fig