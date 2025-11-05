// Main JavaScript for Load Management System

$(document).ready(function() {

    // sweet alert
    // button primary trgger sweet alert

    // Create backdrop element
    if (!$('.sidebar-backdrop').length) {
        $('body').append('<div class="sidebar-backdrop"></div>');
    }

    // Mobile Menu Toggle
    $('#menuToggle').on('click', function(e) {
        e.stopPropagation();
        console.log('Menu toggle clicked');
        
        // Check if mobile or desktop
        if ($(window).width() <= 768) {
            // Mobile behavior
            $('#sidebar').toggleClass('active');
            $('.sidebar-backdrop').toggleClass('active');
            $('body').toggleClass('sidebar-open');
        } else {
            // Desktop behavior
            $('#sidebar').toggleClass('collapsed');
            $('.main-content').toggleClass('expanded');
        }
    });

    // Close sidebar when clicking backdrop (mobile only)
    $(document).on('click', '.sidebar-backdrop', function() {
        if ($(window).width() <= 768) {
            $('#sidebar').removeClass('active');
            $('.sidebar-backdrop').removeClass('active');
            $('body').removeClass('sidebar-open');
        }
    });

    // Close sidebar when clicking outside on mobile
    $(document).on('click', function(e) {
        if ($(window).width() <= 768) {
            if (!$(e.target).closest('#sidebar, #menuToggle').length) {
                $('#sidebar').removeClass('active');
                $('.sidebar-backdrop').removeClass('active');
                $('body').removeClass('sidebar-open');
            }
        }
    });

    // User Dropdown Toggle
    $('#userDropdown').on('click', function(e) {
        e.stopPropagation();
        $('#userMenu').toggleClass('show');
    });

    // Close dropdown when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#userDropdown').length) {
            $('#userMenu').removeClass('show');
        }
    });

    // Active Navigation Link
    $('.nav-link').on('click', function() {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
    });

    // Notification Button
    $('#notificationBtn').on('click', function() {
        // Add your notification logic here
        console.log('Notifications clicked');
    });

    // Form Validation Example
    $('form').on('submit', function(e) {
        let isValid = true;
        
        $(this).find('.form-input.required, .form-select.required').each(function() {
            if ($(this).val() === '') {
                $(this).addClass('error');
                isValid = false;
            } else {
                $(this).removeClass('error');
            }
        });

        if (!isValid) {
            e.preventDefault();
            showAlert('Please fill in all required fields', 'danger');
        }
    });

    // Remove error class on input
    $('.form-input, .form-select').on('input change', function() {
        $(this).removeClass('error');
    });

    // Modal Functions
    window.openModal = function(modalId) {
        $('#' + modalId).fadeIn(200);
        $('body').css('overflow', 'hidden');
    };

    window.closeModal = function(modalId) {
        $('#' + modalId).fadeOut(200);
        $('body').css('overflow', 'auto');
    };

    // Close modal when clicking overlay
    $('.modal-overlay').on('click', function(e) {
        if ($(e.target).hasClass('modal-overlay')) {
            $(this).fadeOut(200);
            $('body').css('overflow', 'auto');
        }
    });

    // Close modal with close button
    $('.modal-close').on('click', function() {
        $(this).closest('.modal-overlay').fadeOut(200);
        $('body').css('overflow', 'auto');
    });

    // Alert Function
    window.showAlert = function(message, type = 'info') {
        const icons = {
            success: 'fa-check-circle',
            danger: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        const alert = $(`
            <div class="alert alert-${type}" style="position: fixed; top: 20px; right: 20px; z-index: 10000; min-width: 300px; animation: slideInRight 0.3s ease;">
                <div class="alert-icon">
                    <i class="fas ${icons[type]}"></i>
                </div>
                <div class="alert-content">
                    <div>${message}</div>
                </div>
            </div>
        `);

        $('body').append(alert);

        setTimeout(function() {
            alert.fadeOut(300, function() {
                $(this).remove();
            });
        }, 3000);
    };

    // Table Row Click
    $('.table tbody tr').on('click', function() {
        $(this).toggleClass('selected');
    });

    // Search Functionality
    $('.header-search input').on('input', function() {
        const searchTerm = $(this).val().toLowerCase();
        // Add your search logic here
        console.log('Searching for:', searchTerm);
    });

    // Smooth Scroll
    $('a[href^="#"]').on('click', function(e) {
        const href = this.getAttribute('href');
        // Only process if href is not just "#"
        if (href && href !== '#' && href.length > 1) {
            const target = $(href);
            if (target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 100
                }, 500);
            }
        }
    });

    // Loading Spinner
    window.showLoading = function() {
        const spinner = $(`
            <div id="loadingOverlay" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 99999;">
                <div class="spinner"></div>
            </div>
        `);
        $('body').append(spinner);
    };

    window.hideLoading = function() {
        $('#loadingOverlay').fadeOut(200, function() {
            $(this).remove();
        });
    };

    // Confirm Dialog
    window.confirmAction = function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    };

    // Copy to Clipboard
    window.copyToClipboard = function(text) {
        const temp = $('<input>');
        $('body').append(temp);
        temp.val(text).select();
        document.execCommand('copy');
        temp.remove();
        showAlert('Copied to clipboard!', 'success');
    };

    // Format Currency
    window.formatCurrency = function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    // Format Date
    window.formatDate = function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    // Debounce Function
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    // Initialize Tooltips (if needed)
    $('[data-tooltip]').hover(
        function() {
            const text = $(this).attr('data-tooltip');
            const tooltip = $(`<div class="tooltip">${text}</div>`);
            $('body').append(tooltip);
            
            const pos = $(this).offset();
            tooltip.css({
                top: pos.top - tooltip.outerHeight() - 10,
                left: pos.left + ($(this).outerWidth() / 2) - (tooltip.outerWidth() / 2)
            });
        },
        function() {
            $('.tooltip').remove();
        }
    );

    // Print Page
    window.printPage = function() {
        window.print();
    };

    // Export to CSV (basic example)
    window.exportTableToCSV = function(tableId, filename) {
        const csv = [];
        const rows = document.querySelectorAll(`#${tableId} tr`);
        
        for (let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll('td, th');
            
            for (let j = 0; j < cols.length; j++) {
                row.push(cols[j].innerText);
            }
            
            csv.push(row.join(','));
        }
        
        const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    };

    // Console welcome message
    console.log('%c Load Management System ', 'background: #4f46e5; color: white; font-size: 16px; padding: 10px;');
    console.log('%c Dashboard loaded successfully! ', 'color: #10b981; font-size: 12px;');
});

// Add CSS animation for alerts
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .tooltip {
        position: absolute;
        background: var(--bg-dark);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        z-index: 10000;
        pointer-events: none;
        white-space: nowrap;
    }
    
    .table tbody tr.selected {
        background-color: var(--primary-light) !important;
    }
`;
document.head.appendChild(style);
