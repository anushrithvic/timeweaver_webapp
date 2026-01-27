// Initial Data Load from LocalStorage
let facultyList = JSON.parse(localStorage.getItem('tw_faculty')) || [
    { id: '1', name: 'Dr. Sarah Thorne', dept: 'CS', currentLoad: 14, maxLoad: 18 },
    { id: '2', name: 'Prof. Alan Turing', dept: 'CS', currentLoad: 10, maxLoad: 12 }
];

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
const hours = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'];

// --- CORE FUNCTIONS ---

// 1. Save and Update Data
function syncStorage() {
    localStorage.setItem('tw_faculty', JSON.stringify(facultyList));
    renderFacultyTable();
    updateDashboardStats();
}

// 2. Add Faculty via Modal
function handleAddFaculty(event) {
    event.preventDefault();
    const newFaculty = {
        id: Date.now().toString(),
        name: document.getElementById('facName').value,
        dept: document.getElementById('facDept').value,
        maxLoad: parseInt(document.getElementById('facMax').value),
        currentLoad: 0
    };

    facultyList.push(newFaculty);
    syncStorage();
    closeModal();
    event.target.reset();
}

// 3. Render the Faculty Management Table
function renderFacultyTable() {
    const container = document.getElementById('facultyTableBody');
    if (!container) return;

    container.innerHTML = facultyList.map(f => {
        const loadPercent = Math.min((f.currentLoad / f.maxLoad) * 100, 100);
        const statusColor = f.currentLoad > f.maxLoad ? 'bg-red-500' : 'bg-indigo-600';

        return `
            <tr class="border-b border-slate-100 hover:bg-slate-50 transition">
                <td class="p-4 font-semibold">${f.name}</td>
                <td class="p-4 text-slate-500">${f.dept}</td>
                <td class="p-4">
                    <div class="flex items-center gap-3">
                        <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                            <div class="h-full ${statusColor}" style="width: ${loadPercent}%"></div>
                        </div>
                        <span class="text-xs font-bold">${f.currentLoad}/${f.maxLoad}h</span>
                    </div>
                </td>
                <td class="p-4 text-center">
                    <button onclick="deleteFaculty('${f.id}')" class="text-slate-400 hover:text-red-500">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// 4. Generate Master Timetable Grid
function generateTimetableGrid() {
    const gridBody = document.getElementById('timetableBody');
    if (!gridBody) return;

    gridBody.innerHTML = hours.map(hour => `
        <div class="grid-row">
            <div class="time-cell">${hour}</div>
            ${days.map(day => `
                <div class="slot-cell" data-day="${day}" data-time="${hour}">
                    ${mockClass(day, hour)}
                </div>
            `).join('')}
        </div>
    `).join('');
}

// Helper to show random classes for UI demonstration
function mockClass(day, hour) {
    if (Math.random() > 0.7) {
        return `
            <div class="class-card">
                <div>
                    <h4 class="text-[11px] font-bold text-indigo-700 uppercase">CS302: AI</h4>
                    <p class="text-xs font-bold">Dr. Sarah Thorne</p>
                </div>
                <div class="flex justify-between items-center text-[10px] text-slate-500">
                    <span>Room 402</span>
                    <i class="fas fa-check-circle text-green-500"></i>
                </div>
            </div>
        `;
    }
    return '';
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    renderFacultyTable();
    generateTimetableGrid();
});