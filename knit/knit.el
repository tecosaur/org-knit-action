#!/usr/bin/env sh
":"; exec emacs --quick --script "$0" -- "$@" # -*- mode: emacs-lisp; lexical-binding: t; -*-

(setq debug-on-error t)

(setq gc-cons-threshold 16777216
      gcmh-high-cons-threshold 16777216
      make-backup-files nil)

(pop argv)
(defvar target-file (pop argv))

(defvar tangle-p nil)
(defvar exporter nil)
(defvar eval-p nil)
(defvar eval-forms nil)
(defvar setupfile nil)
(defvar conf-file nil)

(while argv
  (let ((arg (pop argv)))
    (pcase arg
      ("-t" (setq tangle-p t))
      ("-v" (setq eval-p t))
      ("-e" (push (pop argv) eval-forms))
      ("-x" (setq exporter (pop argv)))
      ("-s" (setq setupfile (pop argv)))
      ("-c" (setq conf-file (pop argv))))))

(when (string= target-file "-h")
  (with-temp-buffer
    (insert "Usage: knit.el [FILE] [OPTIONS...]\n\n"
            "Options:\n"
            " -t            Tangle the file\n"
            " -e            Execute code in the file\n"
            " -x EXPORTER   Export function to use\n"
            " -s SETUPFILE  #+setupfile to use\n"
            " -c CONF-FILE  Elisp file to load\n")
    (princ (buffer-string)))
  (kill-emacs 0))

(require 'org)
(require 'ox)

(when conf-file
  (defalias 'y-or-n-p #'ignore)
  (defalias 'yes-or-no-p #'ignore)
  (load conf-file nil t))

(dolist (form eval-forms)
  (eval form t))

(with-temp-buffer
  (let ((buffer-file-name target-file)
        (default-directory (file-name-directory target-file))
        (org-confirm-babel-evaluate nil)
        org-mode-hook org-load-hook)

    (insert-file-contents target-file)

    (goto-char (point-min))

    (when setupfile
      (insert "#+setupfile: " setupfile "\n"))

    (org-mode)

    (when eval-p
      (org-babel-eval-wipe-error-buffer)
      (org-save-outline-visibility t
        (org-babel-map-executables nil
          (condition-case err
              (if (memq (org-element-type (org-element-context))
                        '(babel-call inline-babel-call))
                  (org-babel-lob-execute-maybe)
                (ignore-errors
                  (org-babel-execute-src-block t)))
            (error
             (message "Eval error! %s" (error-message-string err)))))))

    (when tangle-p
      (condition-case err
          (org-babel-tangle nil nil nil)
        (error (message "Tangle error! %s" (error-message-string err)))))

    (when exporter
      (org-export-expand-include-keyword)
      (condition-case err
          (funcall (intern exporter))
        (error
         (message "Export error! %s" (error-message-string err)))))))

(kill-emacs 0)
