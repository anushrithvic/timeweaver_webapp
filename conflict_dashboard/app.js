// Mock Data for Conflicts
const mockConflicts = [
    {
        id: 'C-101',
        type: 'ROOM_DOUBLE_BOOKING',
        severity: 'critical',
        title: 'Room 304 Double Booked',
        description: 'CS-202 (Data Structures) and CS-301 (OS) are scheduled at the same time.',
        time: 'Mon, 10:00 AM - 11:00 AM',
        location: 'Block A, Room 304',
        parties: ['Prof. Smith', 'Prof. Johnson'],
        status: 'open'
    },
    {
        id: 'C-102',
        type: 'FACULTY_OVERLAP',
        severity: 'critical',
        title: 'Faculty Schedule Conflict',
        description: 'Dr. Sarah Thorne is assigned to two classes simultaneously.',
        time: 'Tue, 02:00 PM - 03:30 PM',
        location: 'Labs 1 & 3',
        parties: ['Dr. Sarah Thorne'],
        status: 'open'
    },
    {
        id: 'C-103',
        type: 'CAPACITY_OVERFLOW',
        severity: 'warning',
        title: 'Room Capacity Exceeded',
        description: 'Class size (65) exceeds room capacity (50).',
        time: 'Wed, 09:00 AM',
        location: 'Room 101',
        parties: ['CS Year 1'],
        status: 'open'
    },
    {
        id: 'C-104',
        type: 'SECTION_OVERLAP',
        severity: 'warning',
        title: 'Section Overlap',
        description: 'Section A has two core subjects scheduled consecutively without break.',
        time: 'Thu, 11:00 AM',
        location: 'N/A',
        parties: ['Section A'],
        status: 'open'
    }
];

// Stats Configuration
const stats = {
    critical: 0,
    warnings: 0,
    resolved: 14 // Mocked previous resolved count
};

// DOM Elements
const container = document.getElementById('conflicts-container');
const statCriticalEl = document.getElementById('stat-critical');
const statWarningsEl = document.getElementById('stat-warnings');
const statResolvedEl = document.getElementById('stat-resolved');
const navCountEl = document.getElementById('nav-count');

// Icon Helper
function getIconForType(type) {
    switch (type) {
        case 'ROOM_DOUBLE_BOOKING': return 'fa-building-circle-exclamation';
        case 'FACULTY_OVERLAP': return 'fa-user-clock';
        case 'CAPACITY_OVERFLOW': return 'fa-users-slash';
        default: return 'fa-circle-exclamation';
    }
}

// Render Conflicts
function renderConflicts() {
    container.innerHTML = '';

    // Reset Stats for calculation
    let crit = 0;
    let warn = 0;

    mockConflicts.forEach(conflict => {
        if (conflict.status !== 'open') return;

        if (conflict.severity === 'critical') crit++;
        if (conflict.severity === 'warning') warn++;

        const card = document.createElement('div');
        // Animation class
        card.className = 'bg-white p-5 rounded-xl border border-slate-200 border-l-4 shadow-sm hover:shadow-md transition-all cursor-pointer animate-fade-in group relative';

        // Dynamic border color based on severity
        const borderColor = conflict.severity === 'critical' ? 'border-l-red-500' : 'border-l-amber-500';
        const iconColor = conflict.severity === 'critical' ? 'text-red-500 bg-red-50' : 'text-amber-500 bg-amber-50';
        card.classList.add(borderColor);

        card.innerHTML = `
            <div class="flex items-start gap-4">
                <div class="w-12 h-12 rounded-lg ${iconColor} flex items-center justify-center shrink-0">
                    <i class="fa-solid ${getIconForType(conflict.type)} text-xl"></i>
                </div>
                
                <div class="flex-1">
                    <div class="flex items-center justify-between mb-1">
                        <h4 class="text-slate-800 font-bold text-lg flex items-center gap-2">
                            ${conflict.title}
                            ${conflict.severity === 'critical'
                ? '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-50 text-red-600 border border-red-100 tracking-wider">CRITICAL</span>'
                : '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-600 border border-amber-100 tracking-wider">WARNING</span>'}
                        </h4>
                        <span class="text-slate-400 text-xs font-mono">#${conflict.id}</span>
                    </div>
                    
                    <p class="text-slate-500 text-sm mb-3 font-medium">${conflict.description}</p>
                    
                    <div class="flex flex-wrap items-center gap-4 text-xs text-slate-500 font-semibold">
                        <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-100 px-2 py-1 rounded">
                            <i class="fa-regular fa-clock text-indigo-500"></i> ${conflict.time}
                        </div>
                        <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-100 px-2 py-1 rounded">
                            <i class="fa-solid fa-location-dot text-indigo-500"></i> ${conflict.location}
                        </div>
                        <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-100 px-2 py-1 rounded">
                            <i class="fa-solid fa-users text-indigo-500"></i> ${conflict.parties.join(', ')}
                        </div>
                    </div>
                </div>

                <div class="flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity absolute right-4 top-1/2 -translate-y-1/2 md:static md:opacity-100 md:translate-y-0">
                    <button onclick="resolveConflict('${conflict.id}')" class="p-2 bg-green-50 hover:bg-green-500 text-green-600 hover:text-white rounded-lg transition-colors border border-green-100 hover:border-green-500" title="Mark Resolved">
                        <i class="fa-solid fa-check"></i>
                    </button>
                    <button class="p-2 bg-indigo-50 hover:bg-indigo-600 text-indigo-600 hover:text-white rounded-lg transition-colors border border-indigo-100 hover:border-indigo-600" title="View Details">
                        <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });

    // Update Stats UI
    statCriticalEl.innerText = crit;
    statWarningsEl.innerText = warn;
    statResolvedEl.innerText = stats.resolved;
    navCountEl.innerText = crit + warn;
}

// Action: Resolve Conflict
window.resolveConflict = function (id) {
    const idx = mockConflicts.findIndex(c => c.id === id);
    if (idx !== -1) {
        mockConflicts[idx].status = 'resolved';
        stats.resolved++;

        // Re-render with animation
        renderConflicts();

        console.log(`Conflict ${id} resolved`);
    }
};

// Initial Render
document.addEventListener('DOMContentLoaded', () => {
    // Add simple fade-in CSS dynamically
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeInUp 0.4s ease-out forwards;
        }
    `;
    document.head.appendChild(style);

    setTimeout(renderConflicts, 500); // Simulate network delay
});
