with open("hamro_hospital/templates/dashboard_base.html", "r") as f:
    code = f.read()

# Add the global modal at the end of the app-shell
modal = """

    <!-- Global Amount Modal -->
    <div class="modal fade" id="valueModal" tabindex="-1">
      <div class="modal-dialog modal-sm modal-dialog-centered">
        <div class="modal-content text-center border-0 shadow-lg" style="border-radius: var(--radius-lg);">
          <div class="modal-header border-0 pb-0">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body pb-4">
            <p class="text-muted mb-1 fw-bold" id="valueModalLabel"></p>
            <h3 class="value-modal-amount mb-0" id="valueModalAmount"></h3>
          </div>
        </div>
      </div>
    </div>
    <script>
    function showFullValue(label, amount) {
        document.getElementById('valueModalLabel').innerText = label;
        document.getElementById('valueModalAmount').innerText = amount;
        new bootstrap.Modal(document.getElementById('valueModal')).show();
    }
    </script>
</div>
"""
code = code.replace("</div>\n{% endblock %}", modal + "{% endblock %}")

# Add back button next to dashboard title
header_old = "<h1>{% block page_title %}Dashboard{% endblock %}</h1>"
header_new = """<div class="d-flex align-items-center gap-2">
                    <button type="button" class="btn btn-sm btn-outline-secondary rounded-circle px-2 py-1" onclick="history.back()" title="Go Back">
                        <i class="bi bi-arrow-left"></i>
                    </button>
                    <h1>{% block page_title %}Dashboard{% endblock %}</h1>
                </div>"""
code = code.replace(header_old, header_new)

with open("hamro_hospital/templates/dashboard_base.html", "w") as f:
    f.write(code)
