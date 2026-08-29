import os
import subprocess
import zipfile

def verify_all():
    # 1. Pure Prod LOC
    exclude_dirs = {'.git', 'node_modules', 'dist', 'build', 'tests', 'test', '__pycache__', '.pytest_cache', 'scripts', 'coverage', '.system_generated', 'logs'}
    prod_extensions = {'.ts', '.js', '.py', '.go', '.rs', '.java', '.cs'}
    total_loc = 0
    file_count = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith('.test') and not d.startswith('.')]
        if any(part in ('tests', 'test', '__tests__') for part in root.replace('\\', '/').split('/')):
            continue
        for f in files:
            if f.endswith(('.test.ts', '.spec.ts', '.test.js', '.spec.js', '.test.py', 'test_*.py')) or f.startswith('test_'):
                continue
            ext = os.path.splitext(f)[1]
            if ext in prod_extensions:
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                        lines = len([line for line in fp if line.strip()])
                        total_loc += lines
                        file_count += 1
                except Exception:
                    pass

    print('==================================================')
    print('CRITERIA VERIFICATION REPORT:')
    print('==================================================')
    loc_status = "PASS" if total_loc >= 50000 else "FAIL"
    print(f'1. Pure Production LOC: {total_loc} lines across {file_count} files (Required: >= 50,000) -> {loc_status}')

    # 2. Git Commits & PRs
    res_commits = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], capture_output=True, text=True)
    commit_count = int(res_commits.stdout.strip()) if res_commits.returncode == 0 else 0
    commit_status = "PASS" if commit_count >= 5 else "FAIL"
    print(f'2. Git Commits: {commit_count} commits (Required: >= 5) -> {commit_status}')

    res_merges = subprocess.run(['git', 'log', '--merges', '--oneline'], capture_output=True, text=True)
    merges = [m for m in res_merges.stdout.strip().splitlines() if m.strip()]
    merge_status = "PASS" if len(merges) >= 4 else "FAIL"
    print(f'3. Pull Request Merges: {len(merges)} merge commits (Required: >= 4) -> {merge_status}')

    # 4. Zip File
    zip_path = 'novacommerce-microservices.zip'
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            git_count = len([f for f in zf.namelist() if f.startswith('.git/')])
            zip_status = "PASS" if git_count > 0 else "FAIL"
            print(f'4. Zip Archive: {os.path.getsize(zip_path)/(1024*1024):.2f} MB containing {git_count} .git files -> {zip_status}')
    else:
        print('4. Zip Archive: Missing -> FAIL')

    # 5. License Check
    with open('LICENSE', 'r') as f:
        lic = f.read().upper()
        has_os = any(term in lic for term in ['MIT LICENSE', 'APACHE LICENSE', 'GENERAL PUBLIC LICENSE', 'GNU'])
        lic_status = "PASS" if not has_os else "FAIL"
        print(f'5. Proprietary License: {lic_status}')

    # 6. Env Check
    env_files = [f for f in os.listdir('.') if f.startswith('.env')]
    env_status = "PASS" if len(env_files) == 0 else "FAIL"
    print(f'6. No .env files committed: {env_status}')
    print('==================================================')

if __name__ == '__main__':
    verify_all()
