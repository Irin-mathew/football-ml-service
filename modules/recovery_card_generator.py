# modules/recovery_card_generator.py
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

class RecoveryCardGenerator:
    """Generates visual recovery cards for players"""
    
    def __init__(self):
        print(" Initializing Recovery Card Generator...")
    
    def generate_card(self, recovery_plan, output_path=None):
        """
        Creates visual recovery card
        
        Args:
            recovery_plan: Dictionary from RecoveryPlanner
            output_path: Optional path to save image
        
        Returns:
            matplotlib figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 12))
            ax.axis('off')
            
            # Background color
            fig.patch.set_facecolor('#F5F5F5')
            ax.set_facecolor('#F5F5F5')
            
            # ===== TITLE =====
            title = f"⚕️ PERSONAL RECOVERY PLAN"
            ax.text(0.5, 0.97, title, fontsize=22, fontweight='bold',
                    ha='center', transform=ax.transAxes, color='#2C3E50')
            
            subtitle = f"Based on match analysis of Player #{recovery_plan['player_id']}"
            ax.text(0.5, 0.94, subtitle, fontsize=14,
                    ha='center', transform=ax.transAxes, color='#7F8C8D')
            
            # Horizontal line (FIXED: removed transform parameter)
            ax.axhline(y=0.92, xmin=0.05, xmax=0.95, color='#3498DB', linewidth=2)
            
            # ===== FATIGUE LEVEL =====
            y_pos = 0.88
            
            # Fatigue header with colored box
            fatigue_header = f" FATIGUE LEVEL: {recovery_plan['fatigue_level']}"
            fatigue_score = f"({recovery_plan['fatigue_score']}/{recovery_plan['fatigue_max']})"
            
            # Color based on fatigue
            if 'CRITICAL' in recovery_plan['fatigue_level']:
                fatigue_color = '#E74C3C'  # Red
            elif 'HIGH' in recovery_plan['fatigue_level']:
                fatigue_color = '#E67E22'  # Orange
            elif 'MODERATE' in recovery_plan['fatigue_level']:
                fatigue_color = '#F1C40F'  # Yellow
            else:
                fatigue_color = '#2ECC71'  # Green
            
            ax.text(0.05, y_pos, fatigue_header, fontsize=16, fontweight='bold',
                    transform=ax.transAxes, color=fatigue_color)
            ax.text(0.05 + len(fatigue_header)*0.007, y_pos, fatigue_score, fontsize=14,
                    transform=ax.transAxes, color='#7F8C8D')
            
            # Key metrics (bullet points)
            y_pos -= 0.04
            for metric in recovery_plan['key_metrics']:
                ax.text(0.08, y_pos, f"   • {metric}", fontsize=12,
                        transform=ax.transAxes, color='#2C3E50')
                y_pos -= 0.03
            
            # ===== POSITION INSIGHTS =====
            y_pos -= 0.02
            ax.text(0.05, y_pos, f" POSITION: {recovery_plan['position']}", 
                    fontsize=16, fontweight='bold', transform=ax.transAxes, color='#2C3E50')
            
            y_pos -= 0.04
            for insight in recovery_plan['position_insights']:
                ax.text(0.08, y_pos, f"   • {insight}", fontsize=12,
                        transform=ax.transAxes, color='#34495E')
                y_pos -= 0.03
            
            # ===== RECOVERY PRESCRIPTION =====
            y_pos -= 0.02
            ax.text(0.05, y_pos, " RECOVERY PRESCRIPTION:", 
                    fontsize=16, fontweight='bold', transform=ax.transAxes, color='#2C3E50')
            
            prescription = recovery_plan['recovery_prescription']
            y_pos -= 0.04
            
            # Rest
            ax.text(0.08, y_pos, f" REST: {prescription['rest_days']} days complete rest", 
                    fontsize=13, transform=ax.transAxes, color='#2C3E50')
            y_pos -= 0.03
            
            # Hydration
            ax.text(0.08, y_pos, f" HYDRATION: {prescription['hydration']}", 
                    fontsize=13, transform=ax.transAxes, color='#2C3E50')
            y_pos -= 0.03
            
            # Sleep
            ax.text(0.08, y_pos, f" SLEEP: {prescription['sleep']}", 
                    fontsize=13, transform=ax.transAxes, color='#2C3E50')
            y_pos -= 0.03
            
            # Activities
            if prescription['activities']:
                activities_text = ", ".join(prescription['activities'][:2])
                ax.text(0.08, y_pos, f"RECOVERY: {activities_text}", 
                        fontsize=13, transform=ax.transAxes, color='#2C3E50')
                y_pos -= 0.03
            
            # Nutrition
            if prescription.get('nutrition'):
                nutrition_text = prescription['nutrition'][0] if prescription['nutrition'] else ""
                ax.text(0.08, y_pos, f" NUTRITION: {nutrition_text}", 
                        fontsize=13, transform=ax.transAxes, color='#2C3E50')
                y_pos -= 0.03
            
            # ===== WARNINGS =====
            if recovery_plan['warnings']:
                y_pos -= 0.02
                ax.text(0.05, y_pos, " WARNING:", 
                        fontsize=16, fontweight='bold', transform=ax.transAxes, color='#E74C3C')
                
                y_pos -= 0.04
                for warning in recovery_plan['warnings'][:3]:  # Show max 3 warnings
                    ax.text(0.08, y_pos, f"   • {warning}", fontsize=12,
                            transform=ax.transAxes, color='#E74C3C')
                    y_pos -= 0.03
            
            # ===== RECOVERY TIMELINE =====
            y_pos -= 0.02
            ax.text(0.05, y_pos, " RECOVERY TIMELINE:", 
                    fontsize=16, fontweight='bold', transform=ax.transAxes, color='#2C3E50')
            
            y_pos -= 0.04
            for timeline_item in recovery_plan['timeline'][:5]:  # Show first 5 days
                ax.text(0.08, y_pos, f"   {timeline_item}", fontsize=12,
                        transform=ax.transAxes, color='#34495E')
                y_pos -= 0.03
            
            # ===== FOOTER =====
            footer_y = 0.02
            ax.text(0.5, footer_y, " AI Football Recovery System", 
                    fontsize=10, ha='center', style='italic', color='#7F8C8D',
                    transform=ax.transAxes)
            
            ax.text(0.5, footer_y - 0.02, "Consult medical professional for serious injuries", 
                    fontsize=9, ha='center', color='#95A5A6', transform=ax.transAxes)
            
            # Set limits
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            
            plt.tight_layout(rect=[0, 0.05, 1, 0.98])
            
            # Save if output path provided
            if output_path:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
                print(f" Recovery card saved: {output_path}")
            
            return fig
            
        except Exception as e:
            print(f"⚠️ Error generating recovery card: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_simple_text_report(self, recovery_plan):
        """Generate simple text version for console or logs"""
        report = []
        report.append("=" * 60)
        report.append(f"RECOVERY PLAN - Player #{recovery_plan['player_id']}")
        report.append("=" * 60)
        report.append(f"Fatigue Level: {recovery_plan['fatigue_level']}")
        report.append(f"Position: {recovery_plan['position']}")
        report.append("")
        report.append("KEY METRICS:")
        for metric in recovery_plan['key_metrics']:
            report.append(f"  • {metric}")
        report.append("")
        report.append("RECOVERY PRESCRIPTION:")
        pres = recovery_plan['recovery_prescription']
        report.append(f"  Rest: {pres['rest_days']} days")
        report.append(f"  Hydration: {pres['hydration']}")
        report.append(f"  Sleep: {pres['sleep']}")
        if pres['activities']:
            report.append("  Activities:")
            for activity in pres['activities']:
                report.append(f"    • {activity}")
        if pres.get('nutrition'):
            report.append("  Nutrition:")
            for item in pres['nutrition']:
                report.append(f"    • {item}")
        report.append("")
        if recovery_plan['warnings']:
            report.append("WARNINGS:")
            for warning in recovery_plan['warnings']:
                report.append(f"  ⚠️ {warning}")
        report.append("")
        report.append("TIMELINE (next 3 days):")
        for i, day in enumerate(recovery_plan['timeline'][:3]):
            report.append(f"  {day}")
        report.append("=" * 60)
        
        return "\n".join(report)