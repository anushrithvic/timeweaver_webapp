// Student Logic

let timetableData = [];

document.addEventListener('DOMContentLoaded', () => {
    loadData();
    updateUI();
});

function loadData() {
    timetableData = JSON.parse(localStorage.getItem('timeWeaver_timetable')) || [];
}

function updateUI() {
    renderFullSchedule();
    renderTodaysClasses();
}

function renderFullSchedule() {
    const times = ["09:00", "10:00", "11:00", "12:00", "01:00", "02:00", "03:00"];
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    const container = document.getElementById('student-timetable-body');

    container.innerHTML = times.map(time => `
        <div class="grid grid-cols-6 border-b border-slate-100 min-h-[100px]">
             <div class="p-4 border-r border-slate-100 text-xs font-bold text-slate-400 flex items-center justify-center bg-slate-50/50">
                ${time}
            </div>
            ${days.map(day => {
        const cls = timetableData.find(c => c.day === day && c.time === time);
        // For student view, we might filter by batch if we had that data.
        // For now, we show all classes in the global timetable (assuming one batch for this demo).
        return `
                    <div class="p-2 border-r border-slate-50 relative group transition-colors hover:bg-slate-50/50">
                        ${cls ? `
                            <div class="bg-white border border-slate-200 p-3 rounded-xl h-full shadow-sm hover:border-indigo-300 hover:shadow-md transition-all">
                                <p class="text-[10px] font-black text-indigo-500 uppercase tracking-tight">${cls.subject}</p>
                                <p class="text-xs font-bold text-slate-500 mt-1">${cls.faculty}</p>
                                <div class="flex justify-between items-end mt-2">
                                    <span class="text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">${cls.room}</span>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `;
    }).join('')}
        </div>
    `).join('');
}

function renderTodaysClasses() {
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const currentDayName = days[new Date().getDay()];
    // For demo, if it's weekend, just default to Monday
    const displayDay = (currentDayName === "Sunday" || currentDayName === "Saturday") ? "Monday" : currentDayName;

    document.getElementById('current-day-badge').innerText = displayDay;

    const todaysClasses = timetableData.filter(t => t.day === displayDay).sort((a, b) => a.time.localeCompare(b.time));
    const container = document.getElementById('todays-classes-list');

    if (todaysClasses.length === 0) {
        container.innerHTML = '<p class="text-slate-400 text-center py-4 text-sm font-medium">No classes scheduled for today.</p>';
        return;
    }

    container.innerHTML = todaysClasses.map(cls => `
        <div class="flex items-center gap-4 p-4 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-white hover:shadow-sm transition">
            <div class="w-16 text-center">
                <p class="text-sm font-black text-slate-700">${cls.time}</p>
                <p class="text-[10px] uppercase font-bold text-slate-400">Time</p>
            </div>
            <div class="w-1 h-10 bg-indigo-500 rounded-full"></div>
            <div class="flex-1">
                <h4 class="font-bold text-slate-800 text-sm">${cls.subject}</h4>
                <p class="text-xs text-slate-500 font-medium">${cls.faculty}</p>
            </div>
            <div class="px-3 py-1 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-500 shadow-sm">
                ${cls.room}
            </div>
        </div>
    `).join('');
}

function showPage(pageId) {
    document.querySelectorAll('.page-content').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.sidebar-item').forEach(b => b.classList.remove('active'));
    document.getElementById(`page-${pageId}`).classList.remove('hidden');
    document.getElementById(`btn-${pageId}`).classList.add('active');
}
