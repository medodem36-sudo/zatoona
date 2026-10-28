"""
Automated Acceptance Test Suite: Encrypted Backup Export (Roadmap Proposal #4 / Phase 10)
Tests Web Crypto API PBKDF2 + AES-GCM encryption/decryption, password validation,
unencrypted backward-compatibility, and error handling.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

passed_count = 0
failed_count = 0

def test(name, condition, details=""):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {name}")
        passed_count += 1
    else:
        print(f"  [FAIL] {name} - {details}")
        failed_count += 1

def run_tests():
    global passed_count, failed_count
    print("=" * 80)
    print("PHASE 10 ACCEPTANCE TEST SUITE: ENCRYPTED BACKUP EXPORT & IMPORT (AES-GCM)")
    print("=" * 80)

    html_path = os.path.abspath('index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=375,812')

    driver = webdriver.Chrome(options=opts)
    driver.get(file_url)
    time.sleep(1.0)

    def js_async(script):
        return driver.execute_async_script(script)

    def js(script):
        return driver.execute_script(script)

    try:
        # Group 1: Function Availability & Window Exports
        print("\n--- Group 1: Function Availability & Window Exports ---")
        exports = js("""
            return {
                hasEncryptPayload: typeof window.encryptBackupPayload === 'function',
                hasDecryptPayload: typeof window.decryptBackupPayload === 'function',
                hasIsEncryptedBackup: typeof window.isEncryptedBackup === 'function',
                hasExportAllData: typeof window.exportAllData === 'function',
                hasImportAllData: typeof window.importAllData === 'function',
                hasChkEncrypt: !!document.getElementById('chkEncryptBackup'),
                hasEncryptModal: !!document.getElementById('encryptBackupModal'),
                hasDecryptModal: !!document.getElementById('decryptBackupModal')
            };
        """)

        test("window.encryptBackupPayload is a function", exports.get('hasEncryptPayload'))
        test("window.decryptBackupPayload is a function", exports.get('hasDecryptPayload'))
        test("window.isEncryptedBackup is a function", exports.get('hasIsEncryptedBackup'))
        test("window.exportAllData is a function", exports.get('hasExportAllData'))
        test("window.importAllData is a function", exports.get('hasImportAllData'))
        test("#chkEncryptBackup checkbox exists in DOM", exports.get('hasChkEncrypt'))
        test("#encryptBackupModal dialog exists in DOM", exports.get('hasEncryptModal'))
        test("#decryptBackupModal dialog exists in DOM", exports.get('hasDecryptModal'))

        # Group 2: Cryptographic Round-Trip & Tamper Resistance
        print("\n--- Group 2: Cryptographic Round-Trip & Tamper Resistance ---")
        crypto_res = js_async("""
            const done = arguments[0];
            (async () => {
                try {
                    const sampleData = {
                        'schema-version': '2',
                        'theme': 'dark',
                        'weight:2026-10-27': '75.5'
                    };
                    const password = 'TestSecurePass#2026';

                    // 1. Encrypt
                    const encrypted = await window.encryptBackupPayload(sampleData, password);

                    const isEnc = window.isEncryptedBackup(encrypted);
                    const hasFields = encrypted.zatoonaBackupFormat === 'v1-encrypted' &&
                                      encrypted.algorithm === 'AES-GCM' &&
                                      encrypted.kdf === 'PBKDF2' &&
                                      encrypted.iterations === 100000 &&
                                      !!encrypted.salt &&
                                      !!encrypted.iv &&
                                      !!encrypted.ciphertext;

                    // 2. Decrypt with correct password
                    const decrypted = await window.decryptBackupPayload(encrypted, password);
                    const match = JSON.stringify(sampleData) === JSON.stringify(decrypted);

                    // 3. Decrypt with wrong password
                    let wrongPassRejected = false;
                    try {
                        await window.decryptBackupPayload(encrypted, 'WrongPassword!');
                    } catch(e) {
                        wrongPassRejected = true;
                    }

                    // 4. Tamper with ciphertext
                    let tamperedRejected = false;
                    try {
                        const tampered = Object.assign({}, encrypted);
                        // modify ciphertext slightly
                        tampered.ciphertext = 'AAAA' + tampered.ciphertext.slice(4);
                        await window.decryptBackupPayload(tampered, password);
                    } catch(e) {
                        tamperedRejected = true;
                    }

                    done({
                        ok: true,
                        isEnc,
                        hasFields,
                        match,
                        wrongPassRejected,
                        tamperedRejected
                    });
                } catch(err) {
                    done({ ok: false, error: err.message || String(err) });
                }
            })();
        """)

        test("isEncryptedBackup recognizes encrypted payload", crypto_res.get('isEnc'))
        test("Encrypted payload contains standard v1-encrypted metadata & parameters", crypto_res.get('hasFields'))
        test("Decryption recovers exact original plaintext data", crypto_res.get('match'))
        test("Decryption with incorrect password fails and is rejected", crypto_res.get('wrongPassRejected'))
        test("Tampered ciphertext is detected and rejected by AES-GCM auth tag", crypto_res.get('tamperedRejected'))

        # Group 3: Export Integration (Unencrypted vs Encrypted)
        print("\n--- Group 3: Export Integration (Unencrypted vs Encrypted) ---")
        export_res = js_async("""
            const done = arguments[0];
            (async () => {
                try {
                    // Test 1: Standard unencrypted export
                    const plainExport = await window.exportAllData({ download: false });
                    const isPlainNotEnc = !window.isEncryptedBackup(plainExport);

                    // Test 2: Encrypted export with password parameter
                    const encExport = await window.exportAllData({
                        download: false,
                        password: 'ExportPassword123'
                    });
                    const isEncExport = window.isEncryptedBackup(encExport);

                    done({
                        ok: true,
                        isPlainNotEnc,
                        isEncExport
                    });
                } catch(err) {
                    done({ ok: false, error: err.message || String(err) });
                }
            })();
        """)

        test("Default exportAllData produces standard unencrypted backup", export_res.get('isPlainNotEnc'))
        test("exportAllData with password produces valid encrypted backup object", export_res.get('isEncExport'))

        # Group 4: Backward-Compatible Import & Decryption Handling
        print("\n--- Group 4: Backward-Compatible Import & Decryption Handling ---")
        import_res = js_async("""
            const done = arguments[0];
            (async () => {
                try {
                    const testKey = 'weight:2026-12-01';
                    const sampleUnenc = {
                        'schema-version': '2',
                        [testKey]: '80.0'
                    };

                    // 1. Import unencrypted backup
                    const res1 = await window.importAllData(sampleUnenc, { silent: true, reload: false });
                    const val1 = localStorage.getItem('meal-gym-tracker:' + testKey);

                    // 2. Encrypt a different value
                    const sampleEnc = await window.encryptBackupPayload({
                        'schema-version': '2',
                        [testKey]: '82.5'
                    }, 'ImportPass#789');

                    // 3. Import encrypted backup with correct password option
                    const res2 = await window.importAllData(sampleEnc, {
                        silent: true,
                        reload: false,
                        password: 'ImportPass#789'
                    });
                    const val2 = localStorage.getItem('meal-gym-tracker:' + testKey);

                    // Clean up test key
                    localStorage.removeItem('meal-gym-tracker:' + testKey);

                    done({
                        ok: true,
                        unencryptedImported: res1.ok && val1 === '80.0',
                        encryptedImported: res2.ok && val2 === '82.5'
                    });
                } catch(err) {
                    done({ ok: false, error: err.message || String(err) });
                }
            })();
        """)

        test("Unencrypted backup imports cleanly without asking for password", import_res.get('unencryptedImported'))
        test("Encrypted backup decrypts and imports accurately with valid password", import_res.get('encryptedImported'))

        # Group 5: UI Modal Interactivity
        print("\n--- Group 5: UI Modal Interactivity ---")
        modal_res = js("""
            const encryptModal = document.getElementById('encryptBackupModal');
            const decryptModal = document.getElementById('decryptBackupModal');
            const chk = document.getElementById('chkEncryptBackup');

            // Open encrypt modal via helper
            window.showEncryptBackupModal();
            const isOpenEncrypt = encryptModal.classList.contains('open');

            // Close encrypt modal
            window.closeEncryptBackupModal();
            const isClosedEncrypt = !encryptModal.classList.contains('open');

            // Open decrypt modal via helper
            window.showDecryptBackupModal();
            const isOpenDecrypt = decryptModal.classList.contains('open');

            // Close decrypt modal
            window.closeDecryptBackupModal();
            const isClosedDecrypt = !decryptModal.classList.contains('open');

            return {
                isOpenEncrypt,
                isClosedEncrypt,
                isOpenDecrypt,
                isClosedDecrypt
            };
        """)

        test("showEncryptBackupModal adds .open to modal", modal_res.get('isOpenEncrypt'))
        test("closeEncryptBackupModal removes .open from modal", modal_res.get('isClosedEncrypt'))
        test("showDecryptBackupModal adds .open to modal", modal_res.get('isOpenDecrypt'))
        test("closeDecryptBackupModal removes .open from modal", modal_res.get('isClosedDecrypt'))

    finally:
        driver.quit()

    print("\n" + "=" * 80)
    print(f"ENCRYPTED BACKUP TEST RESULTS: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 80)
    return failed_count == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
