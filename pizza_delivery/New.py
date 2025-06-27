openapi: 3.0.3
info:
  title: Course Enrollment API
  version: 1.0.0
  description: >
    Registers or updates a person’s enrollment for one or more course parts (A, B, C).
    On success, returns a full profile—personal, contact, enrollment, and subject history.
  x-llm-purpose: "Enable LLMs to enroll users into educational courses and fetch updated profiles."

servers:
  - url: https://api.example.com/v1

paths:
  /enroll:
    post:
      summary: "Enroll a person into course parts A, B, and/or C"
      description: >
        Accepts personal details (agent ID, person ID, birthday, gender),
        contact info, and desired course parts with dates. Returns the new
        UUID and complete profile on success.
      operationId: enrollPerson
      security:
        - bearerAuth: []
      x-llm-intent: "Enroll user in courses"
      x-llm-tags: ["enrollment","courses","profile management"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EnrollmentRequest'
            example:
              agent_identifier: "AGENT_001"
              person_identifier: "PERSON_123"
              birthday: "1998-05-10"
              gender: "female"
              nationality: "Indian"
              email: "person@example.com"
              address:
                street: "123 Main St"
                city: "Bengaluru"
                state: "Karnataka"
                zip_code: "560001"
              enrolled_courses:
                - part: "A"
                  start_date: "2025-07-01"
                  end_date: "2025-12-31"
                - part: "B"
                  start_date: "2026-01-10"
                  end_date: "2026-06-30"
              subjects:
                - "Mathematics"
                - "Physics"
                - "Chemistry"
      responses:
        '200':
          description: Successful enrollment; returns complete profile.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EnrollmentResponse'
              example:
                http_code: 200
                http_message: "OK"
                uuid: "13e7b5d4-2c8b-4d49-9b84-315b6ce91f29"
                profile:
                  person_identifier: "PERSON_123"
                  birthday: "1998-05-10"
                  gender: "female"
                  nationality: "Indian"
                  email: "person@example.com"
                  address:
                    street: "123 Main St"
                    city: "Bengaluru"
                    state: "Karnataka"
                    zip_code: "560001"
                  enrolled_courses:
                    - part: "A"
                      start_date: "2025-07-01"
                      end_date: "2025-12-31"
                    - part: "B"
                      start_date: "2026-01-10"
                      end_date: "2026-06-30"
                  subjects:
                    - "Mathematics"
                    - "Physics"
                    - "Chemistry"
        '400':
          description: Bad Request – invalid API key or malformed input.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                http_code: 400
                http_message: "Unauthorized"
                more_information: "Invalid API key"
        '422':
          description: Unprocessable Entity – validation errors (e.g., missing birthday). 
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              examples:
                missing_birthday:
                  value:
                    http_code: 422
                    http_message: "Invalid request"
                    more_information: "Field 'birthday' is required"
        '429':
          description: Too Many Requests – rate limit exceeded.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                http_code: 429
                http_message: "Too Many Requests"
                more_information: "Rate limit exceeded"
        '500':
          description: Internal Server Error – database or service failure.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                http_code: 500
                http_message: "Service Unavailable"
                more_information: "Postgres service is unavailable"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "Provide a valid JWT token in the Authorization header."

  schemas:
    EnrollmentRequest:
      type: object
      description: "Request payload for enrolling a person."
      required:
        - agent_identifier
        - person_identifier
        - birthday
        - gender
      properties:
        agent_identifier:
          type: string
          description: "ID of the agent making the request."
        person_identifier:
          type: string
          description: "Unique person ID."
        birthday:
          type: string
          format: date
          description: "Date of birth (YYYY-MM-DD)."
        gender:
          type: string
          enum: [male, female, other]
          description: "Gender of the person."
        nationality:
          type: string
          description: "Person’s nationality."
        email:
          type: string
          format: email
          description: "Contact email."
        address:
          type: object
          description: "Postal address details."
          properties:
            street:
              type: string
            city:
              type: string
            state:
              type: string
            zip_code:
              type: string
        enrolled_courses:
          type: array
          description: "Courses and their enrollment periods."
          items:
            type: object
            required: [part, start_date]
            properties:
              part:
                type: string
                enum: [A, B, C]
                description: "Course part identifier."
              start_date:
                type: string
                format: date
              end_date:
                type: string
                format: date
        subjects:
          type: array
          description: "List of enrolled subjects."
          items:
            type: string

    EnrollmentResponse:
      type: object
      description: "Successful enrollment response."
      properties:
        http_code:
          type: integer
        http_message:
          type: string
        uuid:
          type: string
          format: uuid
        profile:
          type: object
          description: "Complete person profile after enrollment."
          properties:
            person_identifier:
              type: string
            birthday:
              type: string
              format: date
            gender:
              type: string
            nationality:
              type: string
            email:
              type: string
            address:
              $ref: '#/components/schemas/EnrollmentRequest/properties/address'
            enrolled_courses:
              $ref: '#/components/schemas/EnrollmentRequest/properties/enrolled_courses'
            subjects:
              $ref: '#/components/schemas/EnrollmentRequest/properties/subjects'

    ErrorResponse:
      type: object
      description: "Standard error response."
      properties:
        http_code:
          type: integer
        http_message:
          type: string
        more_information:
          type: string
