#!/usr/bin/env python3
"""
GitHub Push Automation using gh-mywork
Automates repository creation and pushing for AI/ML mastery project

Usage:
    python github_push.py --first-time    # Create repo on GitHub
    python github_push.py                  # Push subsequent updates
"""

import subprocess
import sys
import os
from datetime import datetime


def run_command(cmd, capture_output=True):
    """Execute shell command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=capture_output
        )
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e.stderr if capture_output else e}")
        return None


def get_notebook_count():
    """Count completed notebooks"""
    notebooks = [f for f in os.listdir('.') if f.endswith('.ipynb') and f[0].isdigit()]
    return len(notebooks)


def get_recent_notebooks():
    """Get list of recently modified notebooks"""
    import glob
    notebooks = glob.glob('0*.ipynb')
    notebooks.sort(key=os.path.getmtime, reverse=True)
    return notebooks[:5]  # Return last 5 modified


def create_commit_message():
    """Generate descriptive commit message"""
    notebook_count = get_notebook_count()
    recent = get_recent_notebooks()
    
    msg_lines = [
        f"feat: AI/ML Mastery Progress - {notebook_count} notebooks complete",
        "",
        "Recently updated notebooks:"
    ]
    
    for nb in recent[:3]:
        # Extract concept name from filename
        name = nb.replace('.ipynb', '').replace('_', ' ')
        msg_lines.append(f"  - {name}")
    
    msg_lines.extend([
        "",
        "Comprehensive coverage of:",
        "  • Machine Learning algorithms (foundations to advanced)",
        "  • Post-silicon validation applications (semiconductor testing)",
        "  • Production-ready implementations with sklearn",
        "  • Real-world project templates",
        "",
        "Target: Demonstrating AI/ML mastery for technical recruiters",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ])
    
    return "\n".join(msg_lines)


def create_github_repo():
    """Create GitHub repository using gh-mywork"""
    print("🚀 Creating GitHub repository using gh-mywork...")
    
    # Check if gh-mywork is available
    gh_mywork_check = run_command("which gh-mywork")
    if not gh_mywork_check:
        print("❌ gh-mywork not found. Installing...")
        install_cmd = "cd /Users/rajendarmuddasani/AIML/14_gh-mywork && pip install -e . > /dev/null 2>&1"
        if not run_command(install_cmd, capture_output=False):
            print("❌ Failed to install gh-mywork")
            return False
    
    # Create repository on GitHub using gh-mywork
    workspace_path = os.getcwd()
    
    cmd = (
        f"cd {workspace_path} && "
        f"gh-mywork create ai-ml-data-engg-mastery "
        f"--account posiva "
        f"--from-path . "
        f"--description 'Complete AI/ML/Data Engineering Mastery - 190+ comprehensive notebooks covering foundations to production deployment. Focused on semiconductor post-silicon validation + general ML/AI applications.' "
        f"--topics ai,machine-learning,data-engineering,python,semiconductor,post-silicon-validation,deep-learning,mlops "
        f"--public "
        f"--branch main"
    )
    
    print(f"Executing: gh-mywork create command...")
    result = run_command(cmd, capture_output=False)
    
    if result is not None:
        print("✅ Repository created successfully on GitHub!")
        return True
    else:
        print("⚠️  Repository creation returned error - checking if repo already exists...")
        # Check if push works (repo might already exist)
        return True


def push_to_github(first_time=False):
    """Push changes to GitHub"""
    
    if first_time:
        print("\n📋 First-time setup: Creating repository...")
        if not create_github_repo():
            print("❌ Repository creation failed")
            return False
        print("✅ Repository ready on GitHub")
    
    # Get current git status
    print("\n📊 Checking git status...")
    status = run_command("git status --short")
    if not status or not status.strip():
        print("✅ No changes to commit")
        # Try to push anyway in case there are committed changes
        print("\n🔄 Checking for unpushed commits...")
    
    # Stage changes (only notebooks and README for first push)
    print("\n➕ Staging changes...")
    if first_time:
        # First push: only notebooks and README
        run_command("git add *.ipynb README.md")
    else:
        # Subsequent pushes: all changes
        run_command("git add -A")
    
    # Check if there's anything to commit
    diff = run_command("git diff --cached --quiet")
    
    # Create and commit
    commit_msg = create_commit_message()
    print(f"\n💬 Commit message:\n{commit_msg}\n")
    
    # Commit only if there are changes
    commit_result = run_command(f'git commit -m "{commit_msg}" || echo "Nothing to commit"')
    
    # Push to main branch
    print("\n🚀 Pushing to GitHub main branch...")
    push_result = run_command("git push -u origin main")
    
    if push_result is not None:
        print("\n✅ Successfully pushed to GitHub!")
        print(f"🔗 View at: https://github.com/rajendarmuddasani/ai-ml-data-engg-mastery")
        return True
    else:
        print("\n❌ Push failed")
        return False


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automate GitHub repository creation and pushing"
    )
    parser.add_argument(
        '--first-time',
        action='store_true',
        help='Create repository on GitHub (first time only)'
    )
    
    args = parser.parse_args()
    
    # Change to workspace directory
    workspace = "/Users/rajendarmuddasani/AIML/48_AI_ML_DataEng_Complete_Mastery"
    os.chdir(workspace)
    
    print("=" * 60)
    print("  GitHub Push Automation - AI/ML Complete Mastery")
    print("=" * 60)
    print(f"\n📂 Workspace: {workspace}")
    print(f"📊 Notebooks: {get_notebook_count()} completed")
    
    if args.first_time:
        print("\n🎯 Mode: First-time setup (create repo + push)")
    else:
        print("\n🎯 Mode: Update push (commit + push changes)")
    
    # Execute push
    success = push_to_github(first_time=args.first_time)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Your work is now on GitHub")
        print("=" * 60)
        print("\n🎯 For recruiters to see:")
        print("   https://github.com/rajendarmuddasani/ai-ml-data-engg-mastery")
        print("\n💡 Next push:")
        print("   python github_push.py")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED - See errors above")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
