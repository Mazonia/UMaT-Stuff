import os
from PIL import Image
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette (Dark Midnight Theme)
    COLOR_BG = RGBColor(11, 15, 25)       # #0B0F19 Deep Navy
    COLOR_CARD = RGBColor(30, 41, 59)     # #1E293B Slate Container
    COLOR_CARD_BORDER = RGBColor(51, 65, 85) # #334155 Slate Border
    COLOR_CYAN = RGBColor(56, 189, 248)   # #38BDF8 Header Accent Cyan
    COLOR_WHITE = RGBColor(248, 250, 252) # #F8FAFC Primary Text White
    COLOR_MUTED = RGBColor(148, 163, 184)# #94A3B8 Secondary Text Muted
    COLOR_AMBER = RGBColor(245, 158, 11)  # #F59E0B Highlight Amber
    COLOR_GREEN = RGBColor(16, 185, 129)  # #10B981 Success Green
    COLOR_BADGE_BG = RGBColor(15, 23, 42) # #0F172A Dark Badge

    def set_slide_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_header(slide, category, title, badge=None):
        # Header container
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        if badge:
            r_badge = p0.add_run()
            r_badge.text = f"[{badge}]  "
            r_badge.font.size = Pt(13)
            r_badge.font.bold = True
            r_badge.font.color.rgb = COLOR_AMBER
            r_badge.font.name = 'Calibri'

        r_cat = p0.add_run()
        r_cat.text = category.upper()
        r_cat.font.size = Pt(12)
        r_cat.font.bold = True
        r_cat.font.color.rgb = COLOR_CYAN
        r_cat.font.name = 'Calibri'
        
        p1 = tf.add_paragraph()
        p1.space_before = Pt(4)
        r_title = p1.add_run()
        r_title.text = title
        r_title.font.size = Pt(22)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_WHITE
        r_title.font.name = 'Calibri'

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    def add_text_box(slide, left, top, width, height, title, bullet_points, highlight_text=None):
        add_card(slide, left, top, width, height)
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), width - Inches(0.5), height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_title = tf.paragraphs[0]
        r_t = p_title.add_run()
        r_t.text = title
        r_t.font.size = Pt(17)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_CYAN
        r_t.font.name = 'Calibri'

        for pt in bullet_points:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
            r_bullet = p.add_run()
            r_bullet.text = "• "
            r_bullet.font.size = Pt(13)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = COLOR_AMBER
            
            if isinstance(pt, tuple):
                label, val = pt
                r_lbl = p.add_run()
                r_lbl.text = f"{label}: "
                r_lbl.font.size = Pt(13)
                r_lbl.font.bold = True
                r_lbl.font.color.rgb = COLOR_WHITE
                r_lbl.font.name = 'Calibri'
                
                r_v = p.add_run()
                r_v.text = str(val)
                r_v.font.size = Pt(13)
                r_v.font.color.rgb = COLOR_MUTED
                r_v.font.name = 'Calibri'
            else:
                r_v = p.add_run()
                r_v.text = str(pt)
                r_v.font.size = Pt(13)
                r_v.font.color.rgb = COLOR_WHITE
                r_v.font.name = 'Calibri'

        if highlight_text:
            p_hl = tf.add_paragraph()
            p_hl.space_before = Pt(12)
            r_hl = p_hl.add_run()
            r_hl.text = f"KEY FINDING: {highlight_text}"
            r_hl.font.size = Pt(12)
            r_hl.font.bold = True
            r_hl.font.color.rgb = COLOR_GREEN
            r_hl.font.name = 'Calibri'

    def add_single_image_panel(slide, left, top, width, height, img_path, caption):
        add_card(slide, left, top, width, height)
        
        # Max image dimensions inside card
        caption_h = 0.75 # inches reserved for caption
        max_img_w = width - Inches(0.4)
        max_img_h = height - Inches(0.4) - Inches(caption_h)

        if os.path.exists(img_path):
            with Image.open(img_path) as im:
                orig_w, orig_h = im.size
            
            aspect = orig_w / orig_h
            card_aspect = max_img_w / max_img_h

            if card_aspect > aspect:
                final_h = max_img_h
                final_w = max_img_h * aspect
            else:
                final_w = max_img_w
                final_h = max_img_w / aspect

            img_left = left + (width - final_w) / 2
            img_top = top + Inches(0.2) + (max_img_h - final_h) / 2
            slide.shapes.add_picture(img_path, img_left, img_top, width=final_w, height=final_h)

        # Caption text box below image
        cap_top = top + height - Inches(caption_h)
        cap_box = slide.shapes.add_textbox(left + Inches(0.2), cap_top, width - Inches(0.4), Inches(caption_h - 0.1))
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = caption
        r.font.size = Pt(11)
        r.font.italic = True
        r.font.color.rgb = COLOR_MUTED
        r.font.name = 'Calibri'

    def add_dual_image_panel(slide, left, top, width, height, img1_info, img2_info):
        add_card(slide, left, top, width, height)
        
        half_h = (height - Inches(0.3)) / 2
        
        # Image 1 (Top half)
        add_single_image_panel(slide, left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), half_h - Inches(0.1), img1_info[0], img1_info[1])
        
        # Image 2 (Bottom half)
        add_single_image_panel(slide, left + Inches(0.15), top + half_h + Inches(0.15), width - Inches(0.3), half_h - Inches(0.1), img2_info[0], img2_info[1])

    # ==================== SLIDE 1: Title Slide ====================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1)
    
    # Title box
    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "CY376: NETWORK MONITORING, SECURITY AND AUDITING"
    r0.font.size = Pt(14)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_CYAN
    r0.font.name = 'Calibri'

    p1 = tf.add_paragraph()
    p1.space_before = Pt(16)
    r1 = p1.add_run()
    r1.text = "Simulated Privilege Escalation &\nDomain Compromise Briefing"
    r1.font.size = Pt(36)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_WHITE
    r1.font.name = 'Calibri'

    p2 = tf.add_paragraph()
    p2.space_before = Pt(16)
    r2 = p2.add_run()
    r2.text = "An Assumed-Breach Red Team Assessment of INLANEFREIGHT.LOCAL Domain"
    r2.font.size = Pt(18)
    r2.font.color.rgb = COLOR_MUTED
    r2.font.name = 'Calibri'

    # Divider bar
    add_card(slide1, Inches(1.0), Inches(4.6), Inches(11.333), Inches(0.04), bg_color=COLOR_AMBER, border_color=None)

    # Presenter metadata
    tb_meta = slide1.shapes.add_textbox(Inches(1.0), Inches(4.9), Inches(11.333), Inches(1.5))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    
    pm = tf_m.paragraphs[0]
    rm = pm.add_run()
    rm.text = "Presenter: Enoch Nana Tabi Oduro  |  Index: CY376-2026-REG  |  Track: Red Team Assessment\nTarget Domain: INLANEFREIGHT.LOCAL  |  Assessment Framework: Assumed-Breach Lifecycle"
    rm.font.size = Pt(13)
    rm.font.color.rgb = COLOR_WHITE
    rm.font.name = 'Calibri'

    # ==================== SLIDE 2: Engagement Scope ====================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2)
    add_header(slide2, "CY376 Red Team Briefing", "1. Engagement Scope & Assumed-Breach Strategy")

    add_text_box(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
                 "Assumed-Breach Threat Model",
                 [
                     ("Realistic Adversary Scenario", "Simulates an insider threat or compromised low-privilege employee workstation."),
                     ("Initial Access Vector", "Pre-authenticated foothold established as user 'hporter' (Domain User)."),
                     ("Scope Boundaries", "Active Directory domain controllers, member servers, and network share infrastructure."),
                     ("Zero Prior Privileges", "No administrative rights or privileged group memberships provided upfront.")
                 ],
                 highlight_text="Validates security posture against real-world post-exploitation adversary TTPs.")

    add_text_box(slide2, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.0),
                 "Primary Technical Objectives",
                 [
                     ("Privilege Escalation Validation", "Demonstrate end-to-end lateral movement and privilege escalation to Domain Admin."),
                     ("Misconfiguration Mapping", "Identify excessive ACL delegations, stored credentials, and unsecure services."),
                     ("DCSync Replication", "Exfiltrate directory credentials via NTDS replication rights."),
                     ("Remediation Roadmap", "Provide actionable, prioritized defense-in-depth guidance aligned with CIS Benchmarks.")
                 ],
                 highlight_text="Objective: 100% compromise of INLANEFREIGHT.LOCAL Active Directory forest.")

    # ==================== SLIDE 3: Target Environment ====================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3)
    add_header(slide3, "CY376 Red Team Briefing", "2. Lab Target Environment & Network Architecture")

    add_text_box(slide3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35),
                 "DC01 (172.16.8.3)",
                 [
                     ("Role", "Primary Domain Controller"),
                     ("OS", "Windows Server 2019"),
                     ("Services", "Active Directory DS, Kerberos, LDAP, SMB, DNS")
                 ])

    add_text_box(slide3, Inches(6.8), Inches(1.8), Inches(5.733), Inches(2.35),
                 "MS01 (172.16.8.50)",
                 [
                     ("Role", "Internal Member Server"),
                     ("OS", "Windows Server 2019"),
                     ("Services", "WinRM, Sysax Automation Service, SQL Server")
                 ])

    add_text_box(slide3, Inches(0.8), Inches(4.45), Inches(5.6), Inches(2.35),
                 "DEV01 / DMZ01 (172.16.8.10)",
                 [
                     ("Role", "Web Pivot / Internal Web Server"),
                     ("OS", "Ubuntu 22.04 LTS"),
                     ("Services", "HTTP Apache, SSH, Internal Web Apps")
                 ])

    add_text_box(slide3, Inches(6.8), Inches(4.45), Inches(5.733), Inches(2.35),
                 "Attacker Station (10.10.15.145)",
                 [
                     ("Platform", "Kali Linux Red Team Workstation"),
                     ("Tooling Suite", "NetExec, Impacket, bloodyAD, Mimikatz, BloodHound"),
                     ("Network Path", "Routable subnet to target lab 172.16.8.0/24")
                 ])

    # ==================== SLIDE 4: Attack Chain Summary ====================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4)
    add_header(slide4, "CY376 Red Team Briefing", "3. 12-Stage Attack Chain Overview & Chained Vectors")

    add_text_box(slide4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0),
                 "Chained Attack Progression (hporter -> Domain Admin)",
                 [
                     ("Foothold & Recon (Stages 1-2)", "Validate hporter credentials; BloodHound ACL query identifies ForceChangePassword over ssmalls."),
                     ("ACL Reset & Share Harvesting (Stages 3-4)", "bloodyAD resets ssmalls password; NetExec share spider finds backupadm credentials in backup script."),
                     ("Lateral Movement & LSA Dump (Stages 5-8)", "Evil-WinRM onto MS01 as backupadm; exploit Sysax service for SYSTEM; Mimikatz dumps mssqladm secrets."),
                     ("Kerberoasting & Group Addition (Stages 9-10)", "GenericWrite over ttimmons -> SPN injection & Hashcat crack (Repeat09); GenericAll self-addition to Server Admins."),
                     ("DCSync & Domain Takeover (Stages 11-12)", "DCSync replication dumps Administrator NTLM hash; Pass-the-Hash Evil-WinRM shell on DC01.")
                 ],
                 highlight_text="12 distinct technical stages successfully chained together to achieve total domain takeover.")

    # Helper for Stage slides
    STAGE_PANEL_LEFT = Inches(0.8)
    STAGE_PANEL_TOP = Inches(1.8)
    STAGE_TEXT_W = Inches(5.4)
    STAGE_PANEL_H = Inches(5.0)
    STAGE_IMG_LEFT = Inches(6.4)
    STAGE_IMG_W = Inches(6.133)

    # ==================== SLIDE 5: STAGE 1 ====================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5)
    add_header(slide5, "CY376 Red Team Briefing", "Stage 1: Initial Access & Foothold Verification", badge="STAGE 01")

    add_text_box(slide5, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 1 Details",
                 [
                     ("Objective", "Verify initial assumed-breach credentials for user hporter."),
                     ("Target Host", "DC01 (172.16.8.3) over SMB."),
                     ("Tool Employed", "NetExec (nxc smb 172.16.8.3 -u hporter -p 'Gr8hambino!')"),
                     ("Execution Syntax", "nxc smb 172.16.8.3 -u hporter -p 'Gr8hambino!'"),
                     ("Outcome", "Returned SMB [+] status, confirming valid domain authentication.")
                 ],
                 highlight_text="Foothold established under INLANEFREIGHT\\hporter identity.")

    add_single_image_panel(slide5, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image2.png",
                           "Figure 1: NetExec SMB Credential Verification for hporter against DC01")

    # ==================== SLIDE 6: STAGE 2 ====================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6)
    add_header(slide6, "CY376 Red Team Briefing", "Stage 2: Active Directory Enumeration (BloodHound)", badge="STAGE 02")

    add_text_box(slide6, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 2 Details",
                 [
                     ("Objective", "Enumerate Active Directory ACLs and locate escalation paths from hporter."),
                     ("Tool Employed", "BloodHound / SharpHound ingestor & Cypher query engine."),
                     ("Cypher Query", "MATCH p=(u:User {name:'HPORTER@INLANEFREIGHT.LOCAL'})-[r]->(t) RETURN p"),
                     ("Discovered Abusable Right", "ForceChangePassword ACL over user ssmalls."),
                     ("Significance", "Allows resetting target user password without knowing existing credentials.")
                 ],
                 highlight_text="Path identified: hporter possesses ForceChangePassword authority over ssmalls.")

    add_single_image_panel(slide6, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image3.png",
                           "Figure 2: BloodHound ACL Analysis Revealing ForceChangePassword Right over ssmalls")

    # ==================== SLIDE 7: STAGE 3 ====================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7)
    add_header(slide7, "CY376 Red Team Briefing", "Stage 3: Abuse of ForceChangePassword ACL", badge="STAGE 03")

    add_text_box(slide7, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 3 Details",
                 [
                     ("Objective", "Force reset ssmalls' password over LDAP using bloodyAD."),
                     ("Tool Employed", "bloodyAD & NetExec SMB verification."),
                     ("Command Syntax", "bloodyAD -u hporter -p 'Gr8hambino!' -d inlanefreight.local --host 172.16.8.3 set password ssmalls 'mazoniakid'"),
                     ("Verification Syntax", "nxc smb 172.16.8.3 -u ssmalls -p 'mazoniakid'"),
                     ("Outcome", "LDAP password reset successful; SMB login validated under ssmalls identity.")
                 ],
                 highlight_text="Identity takeover complete: Control of ssmalls account secured.")

    add_single_image_panel(slide7, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image4.png",
                           "Figure 3: Password Reset Execution over ssmalls via bloodyAD and NetExec SMB Verification")

    # ==================== SLIDE 8: STAGE 4 ====================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide8)
    add_header(slide8, "CY376 Red Team Briefing", "Stage 4: File Share Credential Harvesting", badge="STAGE 04")

    add_text_box(slide8, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 4 Details",
                 [
                     ("Objective", "Harvest plaintext credentials from network file shares accessible to ssmalls."),
                     ("Share Enumeration", "NetExec SMB spidering against DC01 ('Department Shares')."),
                     ("Artifact Discovered", "'SQL Express Backup.ps1' backup script in IT directory."),
                     ("Credentials Extracted", "backupadm : !qazXSW@"),
                     ("Risk Factors", "Hardcoded service account credentials stored in unencrypted scripts.")
                 ],
                 highlight_text="Recovered cleartext credentials for backupadm service account.")

    add_dual_image_panel(slide8, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                         ("extracted_images/image5.png", "Figure 4a: SMB Share Spidering Output"),
                         ("extracted_images/image6.png", "Figure 4b: Extraction of Plaintext Credentials from Backup Script"))

    # ==================== SLIDE 9: STAGE 5 ====================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide9)
    add_header(slide9, "CY376 Red Team Briefing", "Stage 5: WinRM Host Discovery & Lateral Movement", badge="STAGE 05")

    add_text_box(slide9, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 5 Details",
                 [
                     ("Objective", "Pivot laterally onto member server MS01 using harvested credentials."),
                     ("Service Discovery", "WinRM (TCP 5985) listening on MS01 (172.16.8.50)."),
                     ("Tool Employed", "Evil-WinRM remote shell client."),
                     ("Execution Syntax", "evil-winrm -i 172.16.8.50 -u backupadm -p '!qazXSW@'"),
                     ("Outcome", "Established interactive Remote PowerShell session on MS01 as backupadm.")
                 ],
                 highlight_text="Lateral movement successful: Interactive shell obtained on MS01.")

    add_single_image_panel(slide9, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image7.png",
                           "Figure 5: Evil-WinRM Remote Interactive Shell Established on MS01 as backupadm")

    # ==================== SLIDE 10: STAGE 6 ====================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide10)
    add_header(slide10, "CY376 Red Team Briefing", "Stage 6: Leftover Deployment Artifact Exposure", badge="STAGE 06")

    add_text_box(slide10, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 6 Details",
                 [
                     ("Objective", "Inspect MS01 file system for leftover OS installation/deployment artifacts."),
                     ("Artifact Located", "C:\\panther\\unattend.xml (Unattended Windows Setup configuration)."),
                     ("Tool Employed", "Evil-WinRM file system inspection (Get-Content C:\\panther\\unattend.xml)."),
                     ("Credentials Recovered", "ilfserveradm : Sys26Admin"),
                     ("Impact", "Unencrypted deployment file contained sensitive administrative credentials.")
                 ],
                 highlight_text="Discovered cleartext credentials for ilfserveradm in Panther setup log.")

    add_single_image_panel(slide10, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image8.png",
                           "Figure 6: Discovery of Plaintext Credentials for ilfserveradm in C:\\panther\\unattend.xml")

    # ==================== SLIDE 11: STAGE 7 ====================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide11)
    add_header(slide11, "CY376 Red Team Briefing", "Stage 7: Local Privilege Escalation on MS01 (Sysax Service)", badge="STAGE 07")

    add_text_box(slide11, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 7 Details",
                 [
                     ("Objective", "Escalate privileges to NT AUTHORITY\\SYSTEM on member server MS01."),
                     ("Vulnerability", "Sysax Automation Service running as SYSTEM with web GUI on TCP 88."),
                     ("Exploitation Method", "Configured Sysax custom event trigger to execute batch script."),
                     ("Batch Script Action", "net localgroup Administrators ilfserveradm /add"),
                     ("Outcome", "ilfserveradm successfully added to MS01 Local Administrators group.")
                 ],
                 highlight_text="Privilege escalation complete: Local Administrative control secured on MS01.")

    add_dual_image_panel(slide11, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                         ("extracted_images/image9.png", "Figure 7: Sysax Automation Service Web Interface"),
                         ("extracted_images/image10.png", "Figure 8: Execution of Custom Batch Script Adding ilfserveradm to Local Admins"))

    # ==================== SLIDE 12: STAGE 8 ====================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide12)
    add_header(slide12, "CY376 Red Team Briefing", "Stage 8: LSA Secrets Dump on MS01 (Autologon Secrets)", badge="STAGE 08")

    add_text_box(slide12, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 8 Details",
                 [
                     ("Objective", "Dump Local Security Authority (LSA) registry secrets from MS01 memory."),
                     ("Prerequisite", "Local Administrator / SYSTEM privileges on MS01."),
                     ("Tool Employed", "Mimikatz lsadump::secrets & Winlogon registry query."),
                     ("Target Account", "mssqladm (SQL Server Administrator)."),
                     ("Credentials Recovered", "mssqladm : DBAilfreight1!")
                 ],
                 highlight_text="LSA memory dump yielded cleartext password for mssqladm.")

    add_single_image_panel(slide12, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image11.png",
                           "Figure 9: Registry Winlogon DefaultUserName Query & Mimikatz LSA Dump for mssqladm")

    # ==================== SLIDE 13: STAGE 9 ====================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide13)
    add_header(slide13, "CY376 Red Team Briefing", "Stage 9: Targeted Kerberoasting via GenericWrite Delegation", badge="STAGE 09")

    add_text_box(slide13, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 9 Details",
                 [
                     ("Objective", "Compromise target user ttimmons via Targeted Kerberoasting."),
                     ("Delegation Right", "mssqladm possessed GenericWrite control over ttimmons object."),
                     ("SPN Injection", "bloodyAD set SPN 'mssql/MS01' on ttimmons account."),
                     ("Ticket Request", "Impacket GetUserSPNs.py requested Kerberos TGS ticket."),
                     ("Offline Cracking", "Hashcat (Mode 13100) cracked TGS hash -> 'Repeat09'.")
                 ],
                 highlight_text="Targeted Kerberoasting successfully compromised ttimmons : Repeat09.")

    add_dual_image_panel(slide13, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                         ("extracted_images/image12.png", "Figure 11: Targeted SPN Injection on ttimmons via bloodyAD"),
                         ("extracted_images/image13.png", "Figure 12: Hashcat Offline TGS Ticket Cracking (Repeat09)"))

    # ==================== SLIDE 14: STAGE 10 ====================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide14)
    add_header(slide14, "CY376 Red Team Briefing", "Stage 10: Privileged Group Self-Addition (Server Admins)", badge="STAGE 10")

    add_text_box(slide14, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 10 Details",
                 [
                     ("Objective", "Elevate ttimmons to a high-privilege domain security group."),
                     ("Abusable ACL", "ttimmons possessed GenericAll control over 'Server Admins' group."),
                     ("Tool Employed", "bloodyAD group membership addition."),
                     ("Execution Syntax", "bloodyAD -u ttimmons -p 'Repeat09' -d inlanefreight.local --host 172.16.8.3 add groupMember 'Server Admins' ttimmons"),
                     ("Inherited Rights", "Server Admins group possesses Directory Replication (DCSync) rights.")
                 ],
                 highlight_text="Self-addition complete: ttimmons joined Server Admins group.")

    add_single_image_panel(slide14, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image14.png",
                           "Figure 13: Group Membership Query Confirming ttimmons Addition to Server Admins Group")

    # ==================== SLIDE 15: STAGE 11 ====================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide15)
    add_header(slide15, "CY376 Red Team Briefing", "Stage 11: DCSync Attack - Full Domain Credential Extraction", badge="STAGE 11")

    add_text_box(slide15, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 11 Details",
                 [
                     ("Objective", "Extract all Active Directory user NTLM hashes via Directory Replication."),
                     ("Attack Technique", "DCSync attack utilizing DS-Replication-Get-Changes-All extended right."),
                     ("Tool Employed", "Impacket secretsdump.py."),
                     ("Execution Syntax", "python3 secretsdump.py inlanefreight.local/ttimmons:'Repeat09'@172.16.8.3"),
                     ("Exfiltrated Hashes", "Administrator NTLM hash: 161cff084477ae097a9f726700ad71a4")
                 ],
                 highlight_text="Full NTDS database dump achieved: All domain hashes exfiltrated.")

    add_single_image_panel(slide15, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image15.png",
                           "Figure 14: Impacket secretsdump.py Performing DCSync Replication Dumping NTLM Hashes")

    # ==================== SLIDE 16: STAGE 12 ====================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide16)
    add_header(slide16, "CY376 Red Team Briefing", "Stage 12: Proof of Domain Compromise (Pass-the-Hash)", badge="STAGE 12")

    add_text_box(slide16, STAGE_PANEL_LEFT, STAGE_PANEL_TOP, STAGE_TEXT_W, STAGE_PANEL_H,
                 "Stage 12 Details",
                 [
                     ("Objective", "Prove 100% full domain compromise by gaining interactive shell on DC01."),
                     ("Attack Technique", "Pass-the-Hash (PtH) authentication over WinRM."),
                     ("Tool Employed", "Evil-WinRM remote shell client."),
                     ("Execution Syntax", "evil-winrm -i 172.16.8.3 -u Administrator -H 161cff084477ae097a9f726700ad71a4"),
                     ("Final Identity", "INLANEFREIGHT\\Administrator (SYSTEM privilege on Domain Controller DC01).")
                 ],
                 highlight_text="100% Domain Compromise Proven: Full interactive Domain Admin shell on DC01.")

    add_single_image_panel(slide16, STAGE_IMG_LEFT, STAGE_PANEL_TOP, STAGE_IMG_W, STAGE_PANEL_H,
                           "extracted_images/image16.png",
                           "Figure 15: BloodHound Full Attack Path Visualizing Chained Escalation to DCSync")

    # ==================== SLIDE 17: Root Cause Analysis Table ====================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide17)
    add_header(slide17, "CY376 Red Team Briefing", "6. Root-Cause Misconfigurations & Chained Risk Analysis")

    add_text_box(slide17, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0),
                 "Chained Vulnerability Impact Summary",
                 [
                     ("Excessive ACL Delegations", "ForceChangePassword, GenericWrite, and GenericAll assigned to standard users enabled unauthorized password resets and SPN injection."),
                     ("Cleartext Credential Exposure", "Hardcoded service passwords in SMB share scripts ('SQL Express Backup.ps1') and unencrypted unattend.xml setup files."),
                     ("Unsecure Third-Party Services", "Sysax Automation Service running under SYSTEM context allowed local privilege escalation via Web GUI batch triggers."),
                     ("Over-Privileged Group ACLs", "Server Admins group possessed Directory Replication (DCSync) rights, allowing non-Domain Admin accounts to dump NTDS database.")
                 ],
                 highlight_text="A single low-privilege breach was amplified into full domain takeover due to cumulative misconfigurations.")

    # ==================== SLIDE 18: Remediation Roadmap ====================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide18)
    add_header(slide18, "CY376 Red Team Briefing", "7. Prioritized Defensive Remediation Roadmap (CIS Benchmarks)")

    add_text_box(slide18, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0),
                 "Defensive Action Plan & CIS Alignment",
                 [
                     ("1. Revoke Directory Replication Rights (CRITICAL)", "Immediately strip GetChanges and GetChangesAll rights from non-DC accounts including Server Admins."),
                     ("2. Remediate Excessive ACL Delegations (HIGH)", "Audit AD ACLs using BloodHound Enterprise; purge ForceChangePassword & GenericWrite on user objects."),
                     ("3. Migrate Service Accounts to gMSAs (HIGH)", "Replace static service passwords with Group Managed Service Accounts (120-char auto-rotated passwords)."),
                     ("4. Enable LSA Protection & Credential Guard (MEDIUM)", "Deploy HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\RunAsPPL=1 to block LSASS memory dumping by Mimikatz."),
                     ("5. Implement Microsoft Tiered Administration (STRATEGIC)", "Enforce administrative tier boundaries (Tier 0 DC, Tier 1 Servers, Tier 2 Endpoints) to prevent credential theft escalation.")
                 ],
                 highlight_text="Priority: Implement immediate DCSync revocation and ACL cleanup within 24 hours.")

    # ==================== SLIDE 19: Conclusion ====================
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide19)
    add_header(slide19, "CY376 Red Team Briefing", "8. Conclusion & Technical Q&A")

    add_text_box(slide19, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0),
                 "Summary of Assessment Key Outcomes",
                 [
                     ("Domain Compromise Proven", "12-stage attack chain successfully executed from low-privilege hporter to full DC01 Administrator."),
                     ("Zero False Positives", "All stages empirically validated with CLI outputs, screenshots, and BloodHound graphs."),
                     ("Actionable Defense Strategy", "Clear prioritised remediation steps provided to break every link in the attack chain."),
                     ("Deliverables Delivered", "Comprehensive Pentest Report (DOCX/PDF) and Executive Briefing Slide Deck (PPTX).")
                 ],
                 highlight_text="Thank you! Open for Questions & Technical Discussion.")

    output_filename = "INLANEFREIGHT_AD_Compromise_Presentation.pptx"
    prs.save(output_filename)
    print(f"Successfully generated modern 19-slide presentation: '{output_filename}'")

if __name__ == "__main__":
    create_presentation()
