"""
Blue-Green Deployment Pattern Example

This file demonstrates the generic traffic switching pattern for blue-green deployments.
Reference this example from RULE.mdc using @examples_blue_green.py syntax.
"""

# ============================================================================
# Blue-Green Deployment Pattern
# ============================================================================

BLUE_SERVICE_MANIFEST = """
apiVersion: v1
kind: Service
metadata:
  name: application-service-blue
spec:
  selector:
    app: application
    version: blue
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
"""

GREEN_SERVICE_MANIFEST = """
apiVersion: v1
kind: Service
metadata:
  name: application-service-green
spec:
  selector:
    app: application
    version: green
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
"""

TRAFFIC_SWITCHER_MANIFEST = """
apiVersion: v1
kind: Service
metadata:
  name: application-service
spec:
  selector:
    app: application
    version: blue  # Switch to 'green' to route traffic to new version
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
"""

# ============================================================================
# Blue-Green Deployment Script Pattern
# ============================================================================

def deploy_green_environment():
    """
    Generic pattern for deploying to green environment.
    
    This demonstrates the blue-green deployment pattern:
    1. Deploy new version to green environment
    2. Run health checks and smoke tests
    3. Switch traffic from blue to green
    4. Monitor for issues
    5. Keep blue environment as backup for quick rollback
    """
    # Step 1: Deploy to green
    # kubectl apply -f green-deployment.yaml
    
    # Step 2: Wait for green to be ready
    # kubectl wait --for=condition=available deployment/app-green --timeout=300s
    
    # Step 3: Run health checks
    # curl http://green-service/health/ready
    
    # Step 4: Switch traffic (update service selector)
    # kubectl patch service app-service -p '{"spec":{"selector":{"version":"green"}}}'
    
    # Step 5: Monitor green environment
    # kubectl logs -f deployment/app-green
    
    pass


def rollback_to_blue():
    """
    Generic pattern for rolling back to blue environment.
    
    This demonstrates the rollback pattern:
    - Switch traffic back to blue by updating service selector
    - Blue environment remains available for instant rollback
    """
    # Switch traffic back to blue
    # kubectl patch service app-service -p '{"spec":{"selector":{"version":"blue"}}}'
    
    pass
