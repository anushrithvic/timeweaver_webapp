# TimeWeaver Project - Module Specifications
## Full-Stack Development Guide for Team Members

**Project**: TimeWeaver - Intelligent Academic Timetable System  
**Architecture**: FastAPI Backend + React/Vue Frontend  
**Team Size**: 5 Students  
**Each Module**: Complete vertical slice (Backend + Frontend + Integration + Testing)

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Prerequisites & Setup](#prerequisites--setup)
3. [Documentation Standards](#documentation-standards)
4. [Module 1: Authentication & User Management](#module-1-authentication--user-management)
5. [Module 2: Academic Setup & Course Management](#module-2-academic-setup--course-management)
6. [Module 3: Timetable Generation & Scheduling](#module-3-timetable-generation--scheduling)
7. [Module 4: Faculty Management & Workload](#module-4-faculty-management--workload)
8. [Module 5: System Monitoring & Admin Dashboard](#module-5-system-monitoring--admin-dashboard)
9. [Testing Requirements](#testing-requirements)
10. [Integration Guidelines](#integration-guidelines)

---

## Project Structure

```
timeweaver_webapp/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/  # Your API files go here
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic validation schemas
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Request/response interceptors
│   │   └── core/              # Auth, security, config
│   ├── tests/                 # Backend tests
│   ├── alembic/               # Database migrations
│   └── requirements.txt
│
└── frontend/                   # React/Vue frontend
    ├── src/
    │   ├── pages/             # Your page components
    │   ├── components/        # Reusable UI components
    │   ├── services/          # API integration layer
    │   ├── utils/             # Helper functions
    │   └── App.jsx
    ├── public/
    └── package.json
```

---

## Prerequisites & Setup

### Common Prerequisites (All Students)

**1. Development Environment**:
```bash
# Install Python 3.11+
python --version

# Install Node.js 18+
node --version
npm --version

# Install PostgreSQL 15+
psql --version
```

**2. Backend Setup** (One-time):
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb timeweaver

# Run migrations
alembic upgrade head

# Create admin user
python -m app.scripts.create_admin
```

**3. Frontend Setup** (One-time):
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**4. Environment Variables**:
Create `backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/timeweaver
SECRET_KEY=your-secret-key-here
DEBUG=True
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Documentation Standards

### Code Comments Pattern

**Backend (Python)**:
```python
"""
Module: [Module Name]
Owner: [Your Name]
Epic: [Epic Number] - [Epic Name]

[Brief description of what this module does]

Dependencies:
    - [list any modules this depends on]

Example:
    [simple usage example]
"""

def function_name(param: type) -> return_type:
    """
    [Brief description of what function does]
    
    Args:
        param: [description]
        
    Returns:
        [description]
        
    Raises:
        HTTPException: [when and why]
        
    Test Coverage: test_[module].py::test_[function_name]
    
    Example:
        >>> function_name("value")
        result
    """
    pass
```

**Frontend (JavaScript/React)**:
```javascript
/**
 * Module: [Component Name]
 * Owner: [Your Name]
 * 
 * [Brief description]
 * 
 * @component
 * @example
 * return (
 *   <ComponentName prop="value" />
 * )
 */
```

### Testing Documentation Pattern

Each student creates `docs/testing_module_[number].md`:

```markdown
# Testing Documentation - Module [Number]: [Name]

**Student Name**: [Your Name]  
**Module**: [Module Name]  
**Testing Tools**: [Tool 1], [Tool 2]

## Tool Selection Rationale
[Why you chose these tools - 2-3 sentences]

## Test Cases Implemented

### Backend Tests
1. **test_[scenario]**: [description]
   - Input: [example]
   - Expected: [result]
   - Status: ✅ Pass

### Frontend Tests
1. **test_[scenario]**: [description]

### Integration Tests
1. **test_[scenario]**: [description]

## Test Coverage
- Backend: [X]%
- Frontend: [Y]%
- Overall: [Z]%

## Running Tests
```bash
# Backend
pytest tests/test_module[number].py -v --cov

# Frontend
npm test -- --coverage
```

## Known Issues
[Any issues or limitations]
```

---

## Module 1: Authentication & User Management

### Owner: Student A

### Status: ✅ **90% Complete** (Backend done, Frontend needed)

### What Has Been Done ✅

**Backend** (All complete):
- ✅ `/backend/app/api/v1/endpoints/auth.py`
  - POST `/api/v1/auth/login`
  - POST `/api/v1/auth/logout`
  - GET `/api/v1/auth/me`
  - POST `/api/v1/auth/refresh`
  - POST `/api/v1/auth/forgot-password`
  - POST `/api/v1/auth/reset-password`

- ✅ `/backend/app/api/v1/endpoints/users.py`
  - POST `/api/v1/users` (admin only)
  - GET `/api/v1/users` (list, admin only)
  - GET `/api/v1/users/{id}` (admin only)
  - PUT `/api/v1/users/{id}` (admin only)
  - DELETE `/api/v1/users/{id}` (soft delete, admin only)
  - GET `/api/v1/users/me/profile`
  - PUT `/api/v1/users/me/profile`
  - PUT `/api/v1/users/me/password`

- ✅ `/backend/app/core/security.py` - JWT, password hashing
- ✅ `/backend/app/core/dependencies.py` - RBAC
- ✅ `/backend/app/models/user.py` - User model
- ✅ `/backend/app/schemas/user.py` - Validation schemas

### What Needs to Be Done ⚠️

**Frontend** (Create these files):

1. **`/frontend/src/pages/Login.jsx`**
   - Login form with username/password
   - Call `/api/v1/auth/login`
   - Store JWT token in localStorage
   - Redirect to dashboard on success

2. **`/frontend/src/pages/Register.jsx`** (Optional - admin creates users)
   
3. **`/frontend/src/pages/ForgotPassword.jsx`**
   - Email input form
   - Call `/api/v1/auth/forgot-password`
   - Show success message with instructions

4. **`/frontend/src/pages/ResetPassword.jsx`**
   - New password form with token from URL
   - Call `/api/v1/auth/reset-password`

5. **`/frontend/src/pages/Profile.jsx`**
   - Display user info
   - Edit profile form (email, full_name)
   - Change password form
   - Call `/api/v1/users/me/profile` and `/api/v1/users/me/password`

6. **`/frontend/src/services/authService.js`**
   ```javascript
   // API integration layer
   export const authService = {
     login: async (username, password) => { /* ... */ },
     logout: async () => { /* ... */ },
     forgotPassword: async (email) => { /* ... */ },
     resetPassword: async (token, newPassword) => { /* ... */ }
   };
   ```

7. **`/frontend/src/components/AuthForms/`**
   - `LoginForm.jsx`
   - `PasswordResetForm.jsx`
   - `ProfileEditForm.jsx`

### Integration Points

- **Provides to all modules**: JWT authentication tokens
- **Used by**: All other modules need auth tokens for API calls

### Testing Tools

**Backend**: `pytest` + `pytest-asyncio`  
**Frontend**: `Jest` + `React Testing Library`

### Test Coverage Requirements

**Backend Tests** (`tests/test_auth.py`):
```python
def test_login_valid_credentials()
def test_login_invalid_credentials()
def test_token_expiration()
def test_forgot_password_valid_email()
def test_reset_password_expired_token()
def test_change_password()
```

**Frontend Tests** (`src/pages/__tests__/Login.test.jsx`):
```javascript
test('displays login form')
test('submits login successfully')
test('shows error on invalid credentials')
test('redirects after successful login')
```

### Deliverables Checklist

- [ ] Frontend pages (Login, Forgot Password, Reset, Profile)
- [ ] Frontend components (forms, buttons)
- [ ] API integration service
- [ ] Backend tests (>90% coverage)
- [ ] Frontend tests (>75% coverage)
- [ ] Testing documentation
- [ ] Module documentation with screenshots

---

## Module 2: Academic Setup & Course Management

### Owner: Student B

### Status: ✅ **90% Complete** (Backend done, Frontend needed)

### What Has Been Done ✅

**Backend** (All complete):
- ✅ `/backend/app/api/v1/endpoints/courses.py` (5 endpoints)
- ✅ `/backend/app/api/v1/endpoints/departments.py` (5 endpoints)
- ✅ `/backend/app/api/v1/endpoints/semesters.py` (5 endpoints)
- ✅ `/backend/app/api/v1/endpoints/sections.py` (5 endpoints)
- ✅ `/backend/app/api/v1/endpoints/elective_groups.py` (5 endpoints)
- ✅ All models and schemas created
- ✅ RBAC protection (admin-only for write operations)

### What Needs to Be Done ⚠️

**Frontend** (Create these files):

1. **`/frontend/src/pages/admin/Courses.jsx`**
   - Table view of all courses
   - Add/Edit/Delete course buttons
   - Filter by department
   - Pagination

2. **`/frontend/src/pages/admin/Departments.jsx`**
   - CRUD interface for departments
   - Show department stats (# of courses, faculty)

3. **`/frontend/src/pages/admin/Semesters.jsx`**
   - List semesters
   - Create new semester
   - Set active semester

4. **`/frontend/src/pages/admin/Sections.jsx`**
   - Manage class sections
   - Link to courses
   - Set capacity

5. **`/frontend/src/components/CourseForm/CourseForm.jsx`**
   ```jsx
   // Modal form for adding/editing courses
   <CourseForm
     onSubmit={handleSubmit}
     initialData={course}
     departments={departments}
   />
   ```

6. **`/frontend/src/components/DataTable/DataTable.jsx`**
   - Reusable table component
   - Sorting, filtering, pagination
   - Action buttons (edit, delete)

7. **`/frontend/src/services/academicService.js`**
   ```javascript
   export const academicService = {
     // Courses
     getCourses: async (skip, limit) => { /* ... */ },
     createCourse: async (courseData) => { /* ... */ },
     updateCourse: async (id, courseData) => { /* ... */ },
     deleteCourse: async (id) => { /* ... */ },
     
     // Departments
     getDepartments: async () => { /* ... */ },
     // ... similar for semesters, sections
   };
   ```

### Integration Points

- **Requires**: Module 1 (auth tokens)
- **Provides to**: Module 3 (course data for timetable generation)
- **Provides to**: Module 4 (courses to assign to faculty)

### Testing Tools

**Backend**: `pytest-postgresql` (database integration testing)  
**Frontend**: `React Testing Library` + `MSW` (Mock Service Worker)

### Test Coverage Requirements

**Backend Tests** (`tests/test_academic.py`):
```python
def test_create_course_with_valid_data()
def test_create_course_duplicate_code()
def test_update_course()
def test_delete_course_cascade_sections()
def test_list_courses_pagination()
def test_course_requires_admin_auth()
```

**Frontend Tests**:
```javascript
test('displays course list')
test('creates new course')
test('edits existing course')
test('deletes course with confirmation')
test('shows error on duplicate course code')
```

### Deliverables Checklist

- [ ] Admin pages for all entities (Courses, Departments, Semesters, Sections)
- [ ] Reusable form components
- [ ] Data table component with CRUD actions
- [ ] API integration service
- [ ] Backend tests (>85% coverage)
- [ ] Frontend tests (>75% coverage)
- [ ] Testing documentation
- [ ] Screenshots of CRUD workflows

---

## Module 3: Timetable Generation & Scheduling

### Owner: Student C

### Status: ⚠️ **20% Complete** (Constraints done, Generator & Frontend needed)

### What Has Been Done ✅

**Backend** (Partial):
- ✅ `/backend/app/api/v1/endpoints/constraints.py` (6 endpoints)
- ✅ `/backend/app/api/v1/endpoints/time_slots.py` (5 endpoints)
- ✅ `/backend/app/api/v1/endpoints/rooms.py` (5 endpoints)
- ✅ `/backend/app/models/constraint.py`
- ✅ `/backend/app/models/room.py`
- ✅ `/backend/app/models/time_slot.py`

### What Needs to Be Done ⚠️

**Backend** (Create these files):

1. **`/backend/app/models/timetable.py`**
   ```python
   class Timetable(Base):
       __tablename__ = "timetables"
       
       id = Column(Integer, primary_key=True)
       semester_id = Column(Integer, ForeignKey("semesters.id"))
       name = Column(String(100))
       is_published = Column(Boolean, default=False)
       status = Column(String(20))  # generating, completed, failed
       generated_at = Column(DateTime)
       
   class TimetableSlot(Base):
       __tablename__ = "timetable_slots"
       
       id = Column(Integer, primary_key=True)
       timetable_id = Column(Integer, ForeignKey("timetables.id"))
       section_id = Column(Integer, ForeignKey("sections.id"))
       room_id = Column(Integer, ForeignKey("rooms.id"))
       time_slot_id = Column(Integer, ForeignKey("time_slots.id"))
       faculty_id = Column(Integer, ForeignKey("faculty.id"))
       day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
   ```

2. **`/backend/app/schemas/timetable.py`**
   ```python
   class TimetableCreate(BaseModel):
       semester_id: int
       name: str
       
   class TimetableSlotResponse(BaseModel):
       section: SectionResponse
       room: RoomResponse
       time_slot: TimeSlotResponse
       faculty: Optional[FacultyResponse]
       day_of_week: int
   ```

3. **`/backend/app/services/timetable_generator.py`** ⭐ **Core Algorithm**
   ```python
   from typing import List
   from app.models import Section, Room, TimeSlot, Constraint
   
   class TimetableGenerator:
       """
       Intelligent timetable generation using constraint satisfaction.
       
       Algorithm: Greedy backtracking with constraint checking
       """
       
       def __init__(self, semester_id: int, db: AsyncSession):
           self.semester_id = semester_id
           self.db = db
           
       async def generate(self) -> Timetable:
           """
           Main generation algorithm.
           
           Steps:
           1. Load all sections, rooms, time slots, constraints
           2. Sort sections by priority (# students, credits)
           3. For each section:
              - Try all room/time combinations
              - Check constraints (no conflicts, room capacity, faculty availability)
              - Assign first valid slot
              - Backtrack if no solution
           4. Return completed timetable
           """
           # Load data
           sections = await self._load_sections()
           rooms = await self._load_rooms()
           time_slots = await self._load_time_slots()
           constraints = await self._load_constraints()
           
           # Initialize timetable
           timetable = Timetable(semester_id=self.semester_id)
           assigned_slots = []
           
           # Sort sections by priority
           sections = self._prioritize_sections(sections)
           
           # Assign each section
           for section in sections:
               slot = await self._find_valid_slot(
                   section, rooms, time_slots, assigned_slots, constraints
               )
               if slot:
                   assigned_slots.append(slot)
               else:
                   # No valid slot found - handle conflict
                   pass
                   
           return timetable
           
       async def _check_constraints(self, slot, constraints):
           """Check if slot violates any constraints"""
           # No room double-booking
           # No faculty double-booking
           # Room capacity >= section capacity
           # Faculty availability
           # Time slot preferences
           pass
   ```

4. **`/backend/app/api/v1/endpoints/timetables.py`**
   ```python
   @router.post("/generate", response_model=TimetableResponse)
   async def generate_timetable(
       request: TimetableCreate,
       db: AsyncSession = Depends(get_db),
       admin: User = Depends(get_current_admin)
   ):
       """
       Generate new timetable for a semester.
       
       This runs the intelligent scheduling algorithm.
       May take 10-30 seconds depending on complexity.
       """
       generator = TimetableGenerator(request.semester_id, db)
       timetable = await generator.generate()
       return timetable
   
   @router.get("/", response_model=List[TimetableResponse])
   async def list_timetables(db: AsyncSession = Depends(get_db)):
       """List all generated timetables"""
       pass
       
   @router.get("/{timetable_id}/slots")
   async def get_timetable_slots(timetable_id: int):
       """Get all slots in a timetable (grid view)"""
       pass
       
   @router.put("/{timetable_id}/publish")
   async def publish_timetable(timetable_id: int):
       """Publish timetable to make visible to students"""
       pass
   ```

**Frontend** (Create these files):

1. **`/frontend/src/pages/admin/GenerateTimetable.jsx`**
   ```jsx
   function GenerateTimetable() {
     return (
       <>
         <h1>Generate Timetable</h1>
         <SelectSemester onChange={setSemester} />
         <Button onClick={handleGenerate}>Generate</Button>
         {isGenerating && <LoadingSpinner />}
         {timetable && <TimetableGrid data={timetable} />}
       </>
     );
   }
   ```

2. **`/frontend/src/pages/student/ViewTimetable.jsx`**
   - Display student's weekly schedule
   - Color-coded by course
   - Show room locations

3. **`/frontend/src/components/TimetableGrid/TimetableGrid.jsx`**
   ```jsx
   // 7x5 grid (days x time slots)
   <TimetableGrid
     slots={timetableSlots}
     editable={false}
   />
   ```

4. **`/frontend/src/components/ConstraintManager/ConstraintList.jsx`**
   - View all constraints
   - Add/edit/delete constraints
   - Mark as hard/soft

5. **`/frontend/src/services/timetableService.js`**
   ```javascript
   export const timetableService = {
     generate: async (semesterId) => {
       // Shows loading state, may take time
       return await api.post('/timetables/generate', { semester_id: semesterId });
     },
     getSlots: async (timetableId) => { /* ... */ },
     publish: async (timetableId) => { /* ... */ }
   };
   ```

### Integration Points

- **Requires**: Module 2 (courses, sections, rooms)
- **Requires**: Module 4 (faculty availability)
- **Provides to**: Module 5 (data for admin dashboard)
- **Provides to**: Students (view timetable)

### Testing Tools

**Backend**: `pytest` + `hypothesis` (property-based testing for algorithm)  
**Frontend**: `Cypress` (E2E testing for generation workflow)

### Test Coverage Requirements

**Backend Tests** (`tests/test_timetable_generator.py`):
```python
# Algorithm tests
def test_no_room_conflicts()
def test_no_faculty_conflicts()
def test_room_capacity_respected()
def test_backtracking_works()

# Property-based tests with hypothesis
@given(sections=st.lists(st.from_type(Section)))
def test_all_sections_assigned(sections):
    """Every section gets a time slot"""
    pass
```

**Frontend E2E Tests** (`cypress/e2e/timetable.cy.js`):
```javascript
describe('Timetable Generation', () => {
  it('generates and displays timetable', () => {
    cy.login('admin');
    cy.visit('/admin/generate-timetable');
    cy.selectSemester('Fall 2024');
    cy.contains('Generate').click();
    cy.get('.timetable-grid', { timeout: 60000 }).should('be.visible');
  });
});
```

### Deliverables Checklist

- [ ] Timetable models and schemas
- [ ] Timetable generation algorithm (core)
- [ ] Timetable API endpoints
- [ ] Database migration for timetable tables
- [ ] Admin page for generation
- [ ] Student timetable view
- [ ] Timetable grid component
- [ ] Constraint manager UI
- [ ] Algorithm tests (>80% coverage)
- [ ] E2E tests for generation workflow
- [ ] Testing documentation
- [ ] Algorithm explanation document

---

## Module 4: Faculty Management & Workload

### Owner: Student D

### Status: ⚠️ **10% Complete** (Models may exist, everything else needed)

### What Has Been Done ✅

- ✅ `/backend/app/models/user.py` (User model with role=FACULTY)
- ✅ Basic faculty ID field in sections

### What Needs to Be Done ⚠️

**Backend** (Create these files):

1. **`/backend/app/models/faculty.py`**
   ```python
   class Faculty(Base):
       __tablename__ = "faculty"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       employee_id = Column(String(20), unique=True)
       department_id = Column(Integer, ForeignKey("departments.id"))
       designation = Column(String(50))  # Professor, Assoc Prof, Asst Prof
       max_hours_per_week = Column(Integer, default=18)
       
   class FacultyPreference(Base):
       __tablename__ = "faculty_preferences"
       
       id = Column(Integer, primary_key=True)
       faculty_id = Column(Integer, ForeignKey("faculty.id"))
       day_of_week = Column(Integer)  # 0-6
       time_slot_id = Column(Integer, ForeignKey("time_slots.id"))
       preference_type = Column(String(20))  # preferred, not_available
   ```

2. **`/backend/app/services/workload_calculator.py`**
   ```python
   class WorkloadCalculator:
       """Calculate faculty teaching hours and workload"""
       
       @staticmethod
       async def calculate_workload(faculty_id: int, semester_id: int, db: AsyncSession):
           """
           Calculate total teaching hours for a faculty member.
           
           Returns:
               {
                   "total_hours": 15,
                   "lecture_hours": 12,
                   "tutorial_hours": 3,
                   "courses": [...]
               }
           """
           # Get all sections assigned to this faculty
           sections = await db.execute(
               select(Section)
               .where(Section.faculty_id == faculty_id)
               .where(Section.semester_id == semester_id)
           )
           
           total_hours = 0
           for section in sections.scalars():
               course = await section.awaitable_attrs.course
               total_hours += course.lecture_hours
               total_hours += course.tutorial_hours
               
           return {
               "total_hours": total_hours,
               "max_hours": faculty.max_hours_per_week,
               "is_overloaded": total_hours > faculty.max_hours_per_week
           }
   ```

3. **`/backend/app/api/v1/endpoints/faculty.py`**
   ```python
   @router.post("/", response_model=FacultyResponse)
   async def create_faculty(
       faculty_data: FacultyCreate,
       admin: User = Depends(get_current_admin)
   ):
       """Create new faculty profile (admin only)"""
       pass
       
   @router.get("/", response_model=List[FacultyResponse])
   async def list_faculty():
       """List all faculty members"""
       pass
       
   @router.get("/{faculty_id}/workload")
   async def get_faculty_workload(faculty_id: int, semester_id: int):
       """Get teaching workload for a faculty member"""
       calculator = WorkloadCalculator()
       return await calculator.calculate_workload(faculty_id, semester_id, db)
   ```

4. **`/backend/app/api/v1/endpoints/faculty_preferences.py`**
   ```python
   @router.post("/")
   async def set_preference(
       pref: FacultyPreferenceCreate,
       current_user: User = Depends(get_current_user)
   ):
       """
       Faculty sets time preference.
       
       Faculty can only set their own preferences.
       Admins can set for anyone.
       """
       pass
       
   @router.get("/{faculty_id}")
   async def get_preferences(faculty_id: int):
       """Get all preferences for a faculty member"""
       pass
   ```

**Frontend** (Create these files):

1. **`/frontend/src/pages/faculty/Dashboard.jsx`**
   ```jsx
   function FacultyDashboard() {
     const { workload, courses, timetable } = useFacultyData();
     
     return (
       <>
         <WorkloadCard data={workload} />
         <CoursesTable courses={courses} />
         <MyTimetable slots={timetable} />
       </>
     );
   }
   ```

2. **`/frontend/src/pages/faculty/Preferences.jsx`**
   ```jsx
   // Weekly grid to mark preferred/unavailable times
   <PreferenceGrid
     preferences={preferences}
     onSlotClick={handleTogglePreference}
   />
   ```

3. **`/frontend/src/pages/admin/FacultyList.jsx`**
   - Table of all faculty
   - Add/edit/delete faculty
   - View workload
   - Assign courses

4. **`/frontend/src/components/WorkloadChart/WorkloadChart.jsx`**
   - Bar chart showing teaching hours
   - Compare to max hours
   - Show warning if overloaded

5. **`/frontend/src/components/PreferenceSelector/WeeklyPreferenceGrid.jsx`**
   - 7x5 grid for time preferences
   - Click to toggle preferred/not-available
   - Color-coded

6. **`/frontend/src/services/facultyService.js`**
   ```javascript
   export const facultyService = {
     getWorkload: async (facultyId, semesterId) => { /* ... */ },
     setPreference: async (facultyId, day, timeSlot, type) => { /* ... */ },
     getFaculty: async (facultyId) => { /* ... */ }
   };
   ```

### Integration Points

- **Requires**: Module 1 (auth for faculty users)
- **Requires**: Module 2 (courses to assign)
- **Provides to**: Module 3 (faculty availability & preferences for timetable generation)

### Testing Tools

**Backend**: `unittest.mock` (for mocking workload calculations)  
**Frontend**: `Jest` + `React Testing Library`

### Test Coverage Requirements

**Backend Tests** (`tests/test_faculty.py`):
```python
def test_create_faculty_profile()
def test_set_time_preference()
def test_workload_calculation()
def test_workload_exceeds_limit()
def test_faculty_can_only_edit_own_preferences()
```

**Frontend Tests**:
```javascript
test('displays faculty workload correctly')
test('sets time preference')
test('shows warning for overloaded faculty')
test('prevents non-faculty from accessing dashboard')
```

### Deliverables Checklist

- [ ] Faculty model and schemas
- [ ] Faculty CRUD API
- [ ] Workload calculator service
- [ ] Faculty preferences API
- [ ] Database migration
- [ ] Faculty dashboard page
- [ ] Preferences management page
- [ ] Admin faculty list page
- [ ] Workload chart component
- [ ] Backend tests (>85% coverage)
- [ ] Frontend tests (>75% coverage)
- [ ] Testing documentation
- [ ] Workload calculation documentation

---

## Module 5: System Monitoring & Admin Dashboard

### Owner: Student E

### Status: ✅ **80% Complete** (Backend done, Frontend needed)

### What Has Been Done ✅

**Backend** (All complete):
- ✅ `/backend/app/middleware/audit_middleware.py`
- ✅ `/backend/app/services/audit_service.py`
- ✅ `/backend/app/api/v1/endpoints/audit_logs.py`
- ✅ Automatic logging of all POST/PUT/DELETE operations
- ✅ Data sanitization (passwords, tokens)
- ✅ Admin-only query API with filters

### What Needs to Be Done ⚠️

**Frontend** (Create these files):

1. **`/frontend/src/pages/admin/Dashboard.jsx`** ⭐ **Main admin page**
   ```jsx
   function AdminDashboard() {
     const stats = useStats();
     
     return (
       <DashboardGrid>
         <StatsCard title="Total Courses" value={stats.courses} />
         <StatsCard title="Faculty Members" value={stats.faculty} />
         <StatsCard title="Active Students" value={stats.students} />
         <StatsCard title="Timetables" value={stats.timetables} />
         
         <ActivityChart data={stats.activity} />
         <RecentAuditLogs logs={recentLogs} />
       </DashboardGrid>
     );
   }
   ```

2. **`/frontend/src/pages/admin/AuditLogs.jsx`**
   ```jsx
   function AuditLogs() {
     const [filters, setFilters] = useState({});
     const { logs, total } = useAuditLogs(filters);
     
     return (
       <>
         <FilterPanel>
           <SelectUser onChange={setFilters} />
           <SelectAction onChange={setFilters} />
           <DateRangePicker onChange={setFilters} />
         </FilterPanel>
         
         <AuditLogTable
           logs={logs}
           total={total}
           onPageChange={handlePageChange}
         />
       </>
     );
   }
   ```

3. **`/frontend/src/components/StatsCards/StatCard.jsx`**
   ```jsx
   function StatCard({ title, value, trend, icon }) {
     return (
       <Card>
         <Icon src={icon} />
         <Title>{title}</Title>
         <Value>{value}</Value>
         {trend && <Trend positive={trend > 0}>{trend}%</Trend>}
       </Card>
     );
   }
   ```

4. **`/frontend/src/components/Charts/ActivityChart.jsx`**
   - Line chart showing daily activity
   - Use Chart.js or Recharts
   - Shows operations per day

5. **`/frontend/src/components/AuditLogTable/AuditLogTable.jsx`**
   - Table with columns: User, Action, Entity, Time, IP, Details
   - Expandable row for request/response details
   - Export to CSV

6. **`/frontend/src/services/auditService.js`**
   ```javascript
   export const auditService = {
     getLogs: async (filters, skip, limit) => {
       const params = new URLSearchParams({
         ...filters,
         skip,
         limit
       });
       return await api.get(`/audit-logs?${params}`);
     },
     
     getLog: async (id) => {
       return await api.get(`/audit-logs/${id}`);
     }
   };
   ```

7. **`/frontend/src/services/statsService.js`**
   ```javascript
   export const statsService = {
     getOverallStats: async () => {
       // Aggregate stats from multiple endpoints
       const [courses, faculty, students, timetables] = await Promise.all([
         api.get('/courses/count'),
         api.get('/faculty/count'),
         api.get('/users?role=student'),
         api.get('/timetables')
       ]);
       
       return {
         courses: courses.total,
         faculty: faculty.total,
         students: students.total,
         timetables: timetables.length
       };
     }
   };
   ```

### Integration Points

- **Monitors**: ALL modules (receives events from middleware)
- **Provides**: System health visibility to admins
- **No dependencies**: Passive monitoring only

### Testing Tools

**Backend**: `pytest-mock` (test middleware captures events)  
**Frontend**: `Jest` + `Cypress` (E2E for dashboard)

### Test Coverage Requirements

**Backend Tests** (`tests/test_audit_middleware.py`):
```python
def test_middleware_captures_post_request()
def test_middleware_sanitizes_password()
def test_middleware_extracts_user_id()
def test_middleware_skips_get_requests()
def test_query_logs_with_filters()
```

**Frontend E2E Tests** (`cypress/e2e/admin_dashboard.cy.js`):
```javascript
describe('Admin Dashboard', () => {
  it('displays all stats correctly', () => {
    cy.login('admin');
    cy.visit('/admin/dashboard');
    cy.get('[data-test="stat-courses"]').should('contain', '42');
    cy.get('[data-test="activity-chart"]').should('be.visible');
  });
  
  it('filters audit logs', () => {
    cy.visit('/admin/audit-logs');
    cy.selectUser('John Doe');
    cy.get('.audit-log-table tr').should('have.length', 5);
  });
});
```

### Deliverables Checklist

- [ ] Admin dashboard page with stats
- [ ] Audit logs query page
- [ ] Stats cards component
- [ ] Activity chart component
- [ ] Audit log table component
- [ ] Filter panel component
- [ ] Backend tests (>85% coverage)
- [ ] Frontend E2E tests
- [ ] Testing documentation
- [ ] Dashboard screenshots

---

## Testing Requirements

### Testing Tools by Module

| Module | Backend Tool | Frontend Tool | Integration/E2E |
|--------|-------------|---------------|-----------------|
| 1. Auth | `pytest` | `Jest` | Manual testing |
| 2. Academic | `pytest-postgresql` | `React Testing Library` | Manual testing |
| 3. Timetable | `pytest` + `hypothesis` | `Cypress` | Cypress E2E |
| 4. Faculty | `unittest.mock` | `Jest` | Manual testing |
| 5. Dashboard | `pytest-mock` | `Jest` + `Cypress` | Cypress E2E |

### Coverage Targets

**Backend**: 80-90% line coverage  
**Frontend**: 75%+ component coverage  
**Integration**: At least 5 E2E scenarios per module

### Common Testing Commands

```bash
# Backend tests
cd backend
pytest tests/test_module[X].py -v --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage

# E2E tests (Cypress)
npm run cypress:open
```

---

## Integration Guidelines

### API Communication Pattern

**All frontend API calls should**:
1. Include JWT token in Authorization header
2. Handle loading states
3. Handle errors gracefully
4. Show success/error notifications

**Example**:
```javascript
// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// Add token to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors globally
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Database Migration Workflow

When adding new models:
```bash
cd backend

# Create migration
alembic revision -m "add_[model_name]_table"

# Edit migration file in alembic/versions/
# Add upgrade() and downgrade() operations

# Apply migration
alembic upgrade head

# Test rollback
alembic downgrade -1
alembic upgrade head
```

### Code Review Checklist

Before submitting your module:
- [ ] All code has docstring comments
- [ ] Backend tests pass with >80% coverage
- [ ] Frontend tests pass with >75% coverage
- [ ] No console errors in browser
- [ ] API endpoints return proper status codes
- [ ] Error messages are user-friendly
- [ ] Loading states are shown during API calls
- [ ] Forms validate input before submission
- [ ] Testing documentation is complete
- [ ] Screenshots/demo video recorded

---

## Timeline & Milestones

### Week 1-2: Foundation (Modules 1, 2, 4)
- Module 1: Frontend authentication pages
- Module 2: Frontend CRUD pages
- Module 4: Faculty models and backend APIs

### Week 3-4: Core Features (Module 3)
- Module 3: Timetable generation algorithm
- Module 3: Timetable frontend

### Week 5: Integration & Dashboard (Module 5)
- Module 5: Admin dashboard and audit logs UI
- All modules: Integration testing

### Week 6: Testing & Documentation
- All modules: Complete test coverage
- All modules: Testing documentation
- Integration testing between modules
- Bug fixes

### Week 7: Final Polish
- Code review
- Documentation review
- Demo preparation
- Presentation slides

---

## Support & Questions

### Common Issues

**"My frontend can't connect to backend"**
- Check backend is running: `http://localhost:8000/docs`
- Check CORS settings in `backend/app/main.py`
- Check API base URL in frontend

**"Database migration fails"**
- Check if database exists: `psql -l`
- Check DATABASE_URL in `.env`
- Try: `alembic downgrade base` then `alembic upgrade head`

**"Tests are failing"**
- Check if database is running
- Check if test database exists
- Run tests individually to isolate issue

### Git Workflow

```bash
# Create feature branch for your module
git checkout -b module-[number]-[your-name]

# Commit regularly with descriptive messages
git commit -m "feat(module-1): add login form component"

# Push to remote
git push origin module-[number]-[your-name]

# Create pull request when ready
```

---

## Conclusion

Each module owner is responsible for:
1. ✅ Backend API implementation
2. ✅ Frontend UI implementation
3. ✅ Integration between frontend and backend
4. ✅ Comprehensive testing (backend + frontend)
5. ✅ Documentation with clear comments
6. ✅ Testing report documenting tool choice and coverage

**Success Criteria**:
- Module works end-to-end (can demo in browser)
- All tests pass with required coverage
- Code is well-documented
- Integration with other modules verified

Good luck! 🚀
